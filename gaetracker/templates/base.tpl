<html>
  <head>
    <title>Simple Tracker</title>
    <link rel="stylesheet" type="text/css" href="/gae-tracker/static/screen.css"/>
    {% if user %}
      <link rel="icon" type="image/jpeg" href="{{ user|gravatar:16 }}"/>
    {% else %}
      <link rel="icon" type="image/vnd.microsoft.icon" href="/gae-tracker/static/favicon.ico"/>
    {% endif %}
    {% if issue.id %}
      <link rel="alternate" type="application/x-wiki" title="Edit" href="{{ path }}?action=edit&amp;id={{ issue.id }}" />
    {% endif %}
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.5.2/jquery.min.js"></script>
    <script type="text/javascript" src="/gae-tracker/static/scripts.js"></script>
  </head>
<body>
<h1>{% block title %}Simple Tracker{% endblock %}</h1>
{% block contents %}No contents.{% endblock %}
</body>
</html>
