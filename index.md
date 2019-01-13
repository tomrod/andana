## Welcome to andana.me

### Andana means Narrative

This blog is dedicated to improving narrative in data science. The topics I plan to address (though certainly not limit to) are

1. Successful communication of data science findings--demystifying the technical, democratizing the hypothesis generation. Empowering the non-technical may put practicing data science clerics into 

2. Tools that assist the narrative

3. Translating the science of Causal Inference into Data Science methods

I welcome your assistance in this journey. Email me @ narrative.wrangler(at)gmail.


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
