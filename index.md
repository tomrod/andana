## Welcome to andana.me

### Andana means Narrative


Andana.me focuses on data science narratives, methods, and tales from the front-lines.
  <a href="https://www.forbes.com/sites/stevedenning/2012/03/09/the-science-of-storytelling/#4f9a68502d8a">Storytelling is part of what makes us human.</a> You participate in and tell stories daily. Sometimes they nest themselves to share something <a href="https://en.wikipedia.org/wiki/Allegory_of_the_Cave">sublime</a>, other times they share something <a href="https://en.wikipedia.org/wiki/Markov_chain#Gambling">highly technical</a>. In no way is the narrative less important to the latter. <a href="https://www.forbes.com/sites/brentdykes/2016/03/31/data-storytelling-the-essential-data-science-skill-everyone-needs/#16820dbf52ad">Narrative is essential.</a> 


  Often, storytelling is a lost art in the data science space -- yet, narratives run decision making in our world. So come and let us learn this lost art of narratives in data science together.

----------

This blog is dedicated to improving narrative in data science. The topics I plan to address (though certainly not limit to) are

1. Successful communication of data science findings--demystifying the technical, democratizing the hypothesis generation. Empowering the non-technical may put practicing data science clerics into 

2. Tools that assist the narrative

3. Translating the science of Causal Inference into Data Science methods

I welcome your assistance in this journey. Email me @ narrative.wrangler(at)gmail.

-----

  {% for post in site.posts %}
  <article>
    <h3>
     <time datetime="{{ post.date | date: "%Y-%m-%d" }}">{{ post.date | date_to_string }}</time> |
      <a href="{{ post.url }}">
        {{ post.title }}
      </a>
    </h3>
  </article>
{% endfor %}
