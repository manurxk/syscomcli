import re

with open('app/templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# We want to replace everything inside:
# <div class="nav accordion" id="accordionSidenav">
# ...
# </div>
# <!-- Sidenav Footer-->

new_sidebar = """                        {% for section in sidebar_items %}
                        
                            {% if section.is_specialist_view %}
                                <!-- ============================================== -->
                                <!-- VISTA EXCLUSIVA ESPECIALISTA                   -->
                                <!-- ============================================== -->
                                {% for group in section.groups %}
                                <div class="sidenav-menu-heading">{{ group.heading }}</div>
                                {% for item in group.items %}
                                <a class="nav-link" href="{{ "{{ url_for(item.endpoint) if item.endpoint else '#' }}" }}">
                                    <div class="nav-link-icon">{% if item.html_icon %}{{ "{{ item.html_icon|safe }}" }}{% else %}<i data-feather="{{ "{{ item.icon }}" }}"></i>{% endif %}</div>
                                    {{ "{{ item.title }}" }}
                                </a>
                                {% endfor %}
                                {% endfor %}
                                
                            {% else %}
                                <!-- ============================================== -->
                                <!-- VISTA ESTÁNDAR PARA DEMÁS ROLES                -->
                                <!-- ============================================== -->
                                <div class="sidenav-menu-heading">{{ "{{ section.heading }}" }}</div>
                                
                                {% for menu in section.menus %}
                                <a class="nav-link collapsed" href="javascript:void(0);" data-bs-toggle="collapse"
                                    data-bs-target="#{{ "{{ menu.id }}" }}" aria-expanded="false" aria-controls="{{ "{{ menu.id }}" }}">
                                    <div class="nav-link-icon"><i data-feather="{{ "{{ menu.icon }}" }}"></i></div>
                                    {{ "{{ menu.title }}" }}
                                    <div class="sidenav-collapse-arrow"><i class="fas fa-angle-down"></i></div>
                                </a>
                                <div class="collapse" id="{{ "{{ menu.id }}" }}" data-bs-parent="#accordionSidenav">
                                    <nav class="sidenav-menu-nested nav {% if menu.submenus %}accordion{% endif %}" {% if menu.submenus %}id="{{ "{{ menu.id }}" }}Nested"{% endif %}>
                                        
                                        {% if menu.submenus %}
                                            {% for submenu in menu.submenus %}
                                            <a class="nav-link collapsed" href="javascript:void(0);" data-bs-toggle="collapse"
                                                data-bs-target="#{{ "{{ submenu.id }}" }}" aria-expanded="false">
                                                {{ "{{ submenu.title }}" }}
                                                <div class="sidenav-collapse-arrow"><i class="fas fa-angle-down"></i></div>
                                            </a>
                                            <div class="collapse" id="{{ "{{ submenu.id }}" }}" data-bs-parent="#{{ "{{ menu.id }}" }}Nested">
                                                <nav class="sidenav-menu-nested nav">
                                                    {% for link in submenu.links %}
                                                    <a class="nav-link" href="{{ "{{ url_for(link.endpoint) if link.endpoint else '#' }}" }}">
                                                        {% if link.html_icon %}{{ "{{ link.html_icon|safe }}" }}{% endif %}{{ "{{ link.title }}" }}
                                                    </a>
                                                    {% endfor %}
                                                </nav>
                                            </div>
                                            {% endfor %}
                                        {% endif %}
                                        
                                        {% if menu.links %}
                                            {% for link in menu.links %}
                                            <a class="nav-link" href="{{ "{{ url_for(link.endpoint) if link.endpoint else '#' }}" }}">
                                                {% if link.html_icon %}{{ "{{ link.html_icon|safe }}" }}{% endif %}{{ "{{ link.title }}" }}
                                            </a>
                                            {% endfor %}
                                        {% endif %}
                                        
                                    </nav>
                                </div>
                                {% endfor %}
                            {% endif %}
                        {% endfor %}"""

# Use regex to find the accordion content
pattern = re.compile(r'(<div class="nav accordion" id="accordionSidenav">\n)(.*?)(^                    </div>\n                </div>\n                <!-- Sidenav Footer-->)', re.DOTALL | re.MULTILINE)

match = pattern.search(content)
if match:
    new_content = content[:match.start(2)] + new_sidebar + '\n' + content[match.start(3):]
    with open('app/templates/base.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SUCCESS")
else:
    print("PATTERN NOT FOUND")

