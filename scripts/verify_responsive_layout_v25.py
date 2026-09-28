#!/usr/bin/env python3
"""Browser-level acceptance for the ND-UX-V2.5 responsive layout contract.

Uses Chrome DevTools Protocol device metrics rather than Chrome's --window-size
alone, because headless Chrome imposes a ~500 CSS-pixel minimum outer window on
some runners. CDP gives us the exact 430/390/320 CSS viewport widths that the
responsive contract promises to support.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile
import time
from typing import Any
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

import websocket


VIEWPORTS = (
    (1920, 1080),
    (1440, 900),
    (1280, 800),
    (1024, 768),
    (768, 1024),
    (430, 932),
    (390, 844),
    (320, 568),
)

PROBES = {
    "home": "/",
    "question": "/questions/workplace-support-great-britain/",
    "resource": "/resources/goblin-tools/",
    "topic": "/understand/autism/",
    "find": "/find/",
    "about": "/about/",
}


class CDP:
    def __init__(self, websocket_url: str) -> None:
        self.ws = websocket.create_connection(
            websocket_url,
            timeout=15,
            origin="http://127.0.0.1",
        )
        self.next_id = 1
        self.events: list[dict[str, Any]] = []

    def close(self) -> None:
        try:
            self.ws.close()
        except Exception:
            pass

    def _recv(self) -> dict[str, Any]:
        raw = self.ws.recv()
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")
        return json.loads(raw)

    def command(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        call_id = self.next_id
        self.next_id += 1
        self.ws.send(json.dumps({"id": call_id, "method": method, "params": params or {}}))
        while True:
            message = self._recv()
            if message.get("id") == call_id:
                if "error" in message:
                    raise RuntimeError(f"CDP {method} failed: {message['error']}")
                return message.get("result", {})
            if "method" in message:
                self.events.append(message)

    def wait_event(self, method: str, timeout: float = 15.0) -> dict[str, Any]:
        deadline = time.monotonic() + timeout
        while True:
            for index, event in enumerate(self.events):
                if event.get("method") == method:
                    return self.events.pop(index)
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError(f"Timed out waiting for CDP event {method}")
            self.ws.settimeout(remaining)
            message = self._recv()
            if message.get("method") == method:
                self.ws.settimeout(15)
                return message
            if "method" in message:
                self.events.append(message)


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _json_request(url: str, method: str = "GET") -> dict[str, Any]:
    request = Request(url, method=method)
    with urlopen(request, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def _wait_for_debugger(port: int, process: subprocess.Popen[bytes]) -> None:
    deadline = time.monotonic() + 15
    endpoint = f"http://127.0.0.1:{port}/json/version"
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"Chrome exited before debugger startup with code {process.returncode}")
        try:
            _json_request(endpoint)
            return
        except (URLError, TimeoutError, ConnectionError, OSError):
            time.sleep(0.1)
    raise TimeoutError("Chrome remote debugger did not become ready")


def _metrics(cdp: CDP) -> dict[str, Any]:
    expression = r"""
(() => {
  const root = document.documentElement;
  const shell = document.querySelector("main.site-shell");
  const heading = document.querySelector(".page-heading h1");
  const secondary = document.querySelector(".question-secondary-grid");
  const template = secondary ? getComputedStyle(secondary).gridTemplateColumns : "none";
  const columns = secondary && template !== "none"
    ? template.trim().split(/\s+/).filter(Boolean).length
    : 0;
  return {
    innerWidth: window.innerWidth,
    clientWidth: root.clientWidth,
    scrollWidth: root.scrollWidth,
    shellWidth: shell ? Math.round(shell.getBoundingClientRect().width) : 0,
    headingWidth: heading ? Math.round(heading.getBoundingClientRect().width) : 0,
    secondaryColumns: columns
  };
})()
"""
    result = cdp.command(
        "Runtime.evaluate",
        {
            "expression": expression,
            "returnByValue": True,
            "awaitPromise": True,
        },
    )
    value = result.get("result", {}).get("value")
    if not isinstance(value, dict):
        raise RuntimeError(f"Responsive metrics did not return an object: {result}")
    return value


def _assert_metrics(name: str, requested_width: int, requested_height: int, metrics: dict[str, Any]) -> str:
    client = int(metrics["clientWidth"])
    inner = int(metrics["innerWidth"])
    scroll = int(metrics["scrollWidth"])
    shell = int(metrics["shellWidth"])
    heading = int(metrics["headingWidth"])
    columns = int(metrics["secondaryColumns"])

    if client != requested_width or inner != requested_width:
        raise AssertionError(
            f"{name} {requested_width}x{requested_height}: exact CSS viewport not achieved "
            f"(inner={inner}, client={client})"
        )

    expected_shell = min(client * 0.90, 1600)
    if abs(shell - expected_shell) > 3:
        raise AssertionError(
            f"{name} {requested_width}x{requested_height}: shell {shell}px != "
            f"90%/1600px target {expected_shell:.1f}px"
        )

    if scroll > client + 1:
        raise AssertionError(
            f"{name} {requested_width}x{requested_height}: horizontal overflow "
            f"scroll={scroll}px client={client}px"
        )

    if heading > shell + 1:
        raise AssertionError(
            f"{name} {requested_width}x{requested_height}: heading exceeds shell "
            f"heading={heading}px shell={shell}px"
        )

    if name == "question":
        if client >= 1024 and heading < shell * 0.80:
            raise AssertionError(
                f"question {requested_width}x{requested_height}: heading remains pencil-narrow "
                f"({heading}px of {shell}px shell)"
            )
        expected_columns = 2 if client >= 1024 else 1
        if columns != expected_columns:
            raise AssertionError(
                f"question {requested_width}x{requested_height}: secondary grid "
                f"columns={columns}, expected={expected_columns}"
            )

    return (
        f"{name} {requested_width}x{requested_height} "
        f"client={client} shell={shell} scroll={scroll} "
        f"heading={heading} secondary_columns={columns}"
    )


def run(base_url: str, output_dir: Path, report_path: Path, chrome_bin: str | None) -> None:
    chrome = chrome_bin or os.environ.get("CHROME_BIN")
    if not chrome:
        chrome = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if not chrome:
        raise RuntimeError("No Chrome/Chromium executable found")

    port = _free_port()
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="nd-responsive-chrome-") as profile:
        process = subprocess.Popen(
            [
                chrome,
                "--headless=new",
                "--no-sandbox",
                "--disable-gpu",
                "--hide-scrollbars",
                "--disable-background-networking",
                "--disable-component-update",
                "--disable-sync",
                "--no-first-run",
                "--disable-features=OptimizationHints,MediaRouter,AutofillServerCommunication",
                "--remote-allow-origins=*",
                f"--remote-debugging-port={port}",
                "--remote-debugging-address=127.0.0.1",
                f"--user-data-dir={profile}",
                "about:blank",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        cdp: CDP | None = None
        try:
            _wait_for_debugger(port, process)
            target = _json_request(
                f"http://127.0.0.1:{port}/json/new?{quote('about:blank', safe='')}",
                method="PUT",
            )
            cdp = CDP(str(target["webSocketDebuggerUrl"]))
            cdp.command("Page.enable")
            cdp.command("Runtime.enable")
            cdp.command("Network.enable")
            cdp.command("Network.setCacheDisabled", {"cacheDisabled": True})

            rows: list[str] = []
            for width, height in VIEWPORTS:
                cdp.command(
                    "Emulation.setDeviceMetricsOverride",
                    {
                        "width": width,
                        "height": height,
                        "deviceScaleFactor": 1,
                        "mobile": False,
                        "screenWidth": width,
                        "screenHeight": height,
                        "screenOrientation": {"type": "portraitPrimary" if height >= width else "landscapePrimary", "angle": 0},
                    },
                )
                for name, route in PROBES.items():
                    url = base_url.rstrip("/") + route
                    cdp.events.clear()
                    cdp.command("Page.navigate", {"url": url})
                    cdp.wait_event("Page.loadEventFired")
                    # Allow layout/style calculation to settle after the load event.
                    time.sleep(0.05)
                    metrics = _metrics(cdp)
                    rows.append(_assert_metrics(name, width, height, metrics))

                    if name == "question":
                        shot = cdp.command(
                            "Page.captureScreenshot",
                            {
                                "format": "png",
                                "fromSurface": True,
                                "captureBeyondViewport": False,
                            },
                        )
                        data = shot.get("data")
                        if not isinstance(data, str) or not data:
                            raise RuntimeError(f"Missing screenshot data for {width}x{height}")
                        (output_dir / f"question-{width}x{height}.png").write_bytes(base64.b64decode(data))

            report_path.write_text("\n".join(rows) + "\n", encoding="utf-8")
            print("\n".join(rows))
        finally:
            if cdp is not None:
                try:
                    cdp.command("Browser.close")
                except Exception:
                    pass
                cdp.close()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--chrome-bin")
    args = parser.parse_args()
    run(args.base_url, args.output_dir, args.report, args.chrome_bin)


if __name__ == "__main__":
    main()
