#!/usr/bin/env python

import base
print base.minify("""
<script>
$(document).ready(function() {
    var a = 2;
});
</script>
<body class="logged_in  env-production linux vis-public">
<a href="#start-of-content" tabindex="1" class="accessibility-aid js-skip-to-content">Skip to content</a>
    <div class="wrapper">

      <div class="header header-logged-in true" role="banner">
  <div class="container clearfix">

    <a class="header-logo-invertocat" href="https://github.com/" data-hotkey="g d" aria-label="Homepage" ga-data-click="Header, go to dashboard, icon:logo">
  <span class="mega-octicon octicon-mark-github"></span>

  <script>
  $(document).ready(function() {
      var b = 1;
      a + c = 2313213213;
  });
  </script>
</a>
""")