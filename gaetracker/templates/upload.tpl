{% extends "base.tpl" %}
{% block contents %}
<form method="post" enctype="multipart/form-data">
  <div class="field">
    <label>Select a JSON file:</label>
    <input type="file" name="dump"/>
  </div>
  <input type="submit"/>
</form>
{% endblock %}
