# Coffee Tasting Session - {{ session_date }}

## Participants

{% for participant in participants %}- {{ participant.name }} ({{ participant.participant_id }})
{% endfor %}

---

{% for coffee in coffees %}
## {{ coffee.name }} ({{ coffee.coffee_id }})

**Origin**: {{ coffee.origin }}  
**Processing Method**: {{ coffee.processing_method }}  
**Roast Level**: {{ coffee.roast_level }}  
**Roast Date**: {{ coffee.roast_date }}  
**Submitted by**: {{ coffee.submitted_by_name }}  
**Flavor Profile**: {{ ', '.join(coffee.flavor_profile) }}

### Average Ratings

| Attribute    | Average Score |
|--------------|---------------|
{% for attribute, score in coffee.average_ratings.items() %}| {{ attribute.capitalize() }} | {{ "%.2f" | format(score) }}      |
{% endfor %}

### Individual Ratings

| Participant       | {% for attribute in rating_attributes %}{{ attribute.capitalize() }} | {% endfor %}
|-------------------|{% for attribute in rating_attributes %}:---:|{% endfor %}
{% for rating in coffee.ratings %}| {{ rating.participant_name }} | {% for attribute in rating_attributes %}{{ rating[attribute] }} | {% endfor %}
{% endfor %}

---

{% endfor %}

## Overall Rankings

| Rank | Coffee                                 | Average Rank |
|------|----------------------------------------|--------------|
{% for rank in overall_rankings %}| {{ loop.index }} | {{ rank.coffee_name }} ({{ rank.session_coffee_id }}) | {{ "%.2f" | format(rank.rank) }} |
{% endfor %}
