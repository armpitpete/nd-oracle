<?php
defined('_JEXEC') or die;

// Joomla owns the rendering and script lifecycle; the existing reviewed
// /media/ndoracle/find.js remains unchanged and executes entirely in-browser.
$assets = $app->getDocument()->getWebAssetManager();
$assets->getRegistry()->addExtensionRegistryFile('mod_ndoracle_find');
$assets->useScript('mod_ndoracle_find.bootstrap');
?>
<div class="nd-parity nd-parity--find nd-oracle-find">
  <section aria-labelledby="find-heading">
    <h2 id="find-heading">What are you looking for?</h2>
    <div class="find-control">
      <div class="find-field">
        <label for="find-input">Search words</label>
        <input aria-describedby="find-help" autocomplete="off" id="find-input" maxlength="500" spellcheck="true" type="search">
      </div>
      <button id="find-button" type="button">Search</button>
    </div>
    <p class="meta" id="find-help">Try “noisy classroom”, “phone calls” or “getting started”. Your words stay in this browser.</p>
  </section>
  <section aria-atomic="false" aria-label="Search results" aria-live="polite" id="find-results" role="region">
    <p>Search results will appear here. A match is not a personal recommendation.</p>
  </section>
  <noscript>
    <section class="boundary-panel">
      <h2>Search needs JavaScript</h2>
      <p>You can still <a href="/questions">browse questions</a>, <a href="/needs">browse by need</a>, or <a href="/a-z">use A–Z</a>.</p>
    </section>
  </noscript>
</div>
