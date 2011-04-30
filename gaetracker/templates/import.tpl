{% extends "base.tpl" %}
{% block contents %}
<form method="post" enctype="multipart/form-data">
  <div class="field">
    <label>Select a JSON file:</label>
    <input type="file" name="dump"/>
  </div>
  <p>This must be a file like the one that you exported earlier.</p>
  <p>Issues will be imported in the background, so it can take some time for them to appear.</p>
  <input type="submit" value="Start importing"/>
</form>
{% endblock %}
