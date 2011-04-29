{% extends "base.tpl" %}
{% block contents %}
<p><a href="{{ path }}?action=submit">Submit new issue</a></p>
<table>
  <thead>
    <tr>
      <th/>
      <th/>
      <th class="id">Id</th>
      <th class="status">Status</th>
      <th class="summary">Summary</th>
      <th class="date">Date</th>
    </tr>
  </thead>
  <tbody>
    {% for issue in issues %}
      <tr>
        <td><input type="checkbox" name="key" value="{{ issue.key }}"/></td>
        <td><img src="{{ issue.owner|gravatar:24 }}" title="{{ issue.owner }}" alt="avatar"/></td>
        <td class="id"><a href="{{ path }}?action=view&amp;id={{ issue.id }}">#{{ issue.id }}</a></td>
        <td class="status">{{ issue.status }}</td>
        <td class="summary"><a href="{{ path }}?action=view&amp;id={{ issue.id }}">{{ issue.summary|escape }}</a></td>
        <td class="date">{{ issue.date_created|date:"d.m.y" }}</td>
      </tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}
