{% extends "base.tpl" %}
{% block title %}New issue{% endblock %}
{% block contents %}
<div id="submit">
  <form method="post">
    <div class="field">
      <label>Summary:</label>
      <input type="text" name="f.summary" class="text"/>
    </div>
    <div class="field">
      <label>Description:</label>
      <textarea name="f.description" class="text"></textarea>
    </div>
    <div class="field">
      <label>Labels:</label>
      <input type="text" name="f.labels" class="text"/>
    </div>
    <input type="submit"/>
  </form>
</div>
{% endblock %}
