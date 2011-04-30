{% extends "base.tpl" %}
{% block contents %}
<p><a href="{{ path }}?action=submit">Submit new issue</a>{% if filter %} or <a href="{{ path }}">reset filter</a>{% endif %}</p>
{% if issues %}
<table>
  <thead>
    <tr>
      <!--
      <th/>
      -->
      <th class="owner">Owner</th>
      <th class="id">Id</th>
      {% for c in columns %}
        <th class="extra">{{ c }}</th>
      {% endfor %}
      <th class="summary">Summary</th>
      <th class="comments">Comments</th>
      <th class="date">Date</th>
    </tr>
  </thead>
  <tbody>
    {% for issue in issues %}
      <tr>
        <!--
        <td><input type="checkbox" name="key" value="{{ issue.key }}"/></td>
        -->
        <td class="owner">{% if issue.owner %}<img src="{{ issue.owner|gravatar:24 }}" title="{{ issue.owner }}" alt="avatar"/>{% endif %}</td>
        <td class="id"><a href="{{ path }}?action=view&amp;id={{ issue.id }}">#{{ issue.id }}</a></td>
        {% for c in columns %}
          <td class="extra">{{ issue|extra_column:c }}</td>
        {% endfor %}
        <td class="summary"><a href="{{ path }}?action=view&amp;id={{ issue.id }}">{{ issue.summary|escape }}</a>{{ issue|extra_labels }}</td>
        <td class="comments">{% if issue.comment_count %}{{ issue.comment_count }}{% endif %}</td>
        <td class="date">{{ issue.date_created|date:"d.m.y" }}</td>
      </tr>
    {% endfor %}
  </tbody>
</table>

<p><a href="{{ path }}?action=export{% if filter %}&amp;label={{ filter|escape }}{% endif %}">Download these issues</a> or <a href="{{ path }}?action=import">upload some</a></p>
{% endif %}
{% endblock %}
