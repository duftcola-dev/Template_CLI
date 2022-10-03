LAYOUT="""
<!DOCTYPE html>
<html lang="en">
<head>
    {% load static %}
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{% static 'css/bootstrap.css' %}">
    <title>Default</title>
</head>
<body class="p-3 m-0 border-0">
    {%include "./_header.html"%}
    {%block body%}{%endblock%}
    {%include "./_footer.html"%}
    <script src="{% static 'js/bootstrap.js' %}"></script>
</body>
</html>        
"""

HEADER="""
<div class="container">
    <div class="py-3 my-4">
        <ul class="nav justify-content-center bg-light">
            <li class="nav-item">
                <h4><a class="nav-link px-2 text-muted" href="#">Default1</a></h4>
            </li>
            <li class="nav-item">
                <h4><a class="nav-link px-2 text-muted" href="#">Default2</a></h4>
            </li>
            <li class="nav-item">
                <h4><a class="nav-link px-2 text-muted" href="#">Default2</a></h4>
            </li>
            <li class="nav-item">
                <h4><a class="nav-link px-2 text-muted" href="#">Default2</a></h4>
            </li>
        </ul>
    </div>
</div>
<br>
"""
FOOTER="""
<div class="container">
    <footer class="py-3 my-4">
        <ul class="nav justify-content-center border-bottom pb-3 mb-3">
            <li class="nav-item">
                <a class="nav-link px-2 text-muted" href="#">Default1</a>
            </li>
            <li class="nav-item">
                <a class="nav-link px-2 text-muted" href="#">Default1</a>
            </li>
            <li class="nav-item">
                <a class="nav-link px-2 text-muted" href="#">Default1</a>
            </li>
            <li class="nav-item">
                <a class="nav-link px-2 text-muted" href="#">Default1</a>
            </li>
        </ul>
        <p class="text-center text-muted">2022</p>
    </footer>
</div>
"""

HOME="""
{%extends "./layout/_layout.html" %}
{%block body%}
<div class="vstack gap-3">
    <h2>Hello world</h2>
</div>
{%endblock%}
"""