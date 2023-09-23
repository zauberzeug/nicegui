from nicegui import ui

def _init_cap(s):
    return " ".join([i.strip().capitalize() for i in s.split("_") if i.strip()])

def _get_var_name(v):
    for name in globals():
        x = eval(name)
        if x is not None and x == v:
            return name
    return ""

def _render_mermaid(var):
    with ui.column():
        ui.label(_init_cap(_get_var_name(var)))
        ui.mermaid(var)
        with ui.expansion('Show', icon='apple'):
            ui.markdown(f"""```{var}```""")


ui.markdown(""" ## Mermaid - A Nice Diagramming Tool
- [Home](https://mermaid.js.org/)
- [Docs](https://mermaid.js.org/intro/)
- [Github](https://github.com/mermaid-js/mermaid)
                        
""")

ui.markdown(""" ### Basic""")
left_to_right_graph = """
    graph LR;
        A --> B;
        A --> C;
"""
top_down_graph_1 = '''
    graph TD;
        女 --> 好;
        子 --> 好;
'''
top_down_graph_2 = '''
    graph TD;
        A --> B & C --> D;
'''

with ui.row():
    with ui.column():
        _render_mermaid(left_to_right_graph)

    with ui.column():
        _render_mermaid(top_down_graph_1)

    with ui.column():
        _render_mermaid(top_down_graph_2)


ui.markdown(""" ### Flowchart """)
flowchart_1 = '''
        graph TD
            A[Enter Chart Definition] --> B(Preview)
            B --> C{decide}
            C --> D[Keep]
            C --> E[Edit Definition]
            E --> B
            D --> F[Save Image and Code]
            F --> B
    '''

flowchart_2 = '''
        flowchart TD
            A[Start] --> B{Is it?}
            B -->|Yes| C[OK]
            C --> D[Rethink]
            D --> B
            B ---->|No| E[End]
    '''

with ui.row():
    _render_mermaid(flowchart_1)

    _render_mermaid(flowchart_2)

ui.markdown(""" ### More [Examples](https://mermaid.js.org/intro/)
           
""")
flowchart_with_htmlLabels = '''
%%{init: {"flowchart": {"htmlLabels": true}} }%%
flowchart LR
    markdown["` goto [Mermaid.js](https://mermaid.js.org/) `"]
    newLines["`Line1
    Line 2
    Line 3`"]
    markdown --> newLines
'''

_render_mermaid(flowchart_with_htmlLabels)

seq_diagram = """
sequenceDiagram
    Alice->>+John: Hello John, how are you?
    Alice->>+John: John, can you hear me?
    John-->>-Alice: Hi Alice, I can hear you!
    John-->>-Alice: I feel great!
"""
_render_mermaid(seq_diagram)

flow_chart_3 = """
flowchart TD
    A[Christmas] -->|Get money| B(Go shopping)
    B --> C{Let me think}
    C -->|One| D[Laptop]
    C -->|Two| E[iPhone]
    C -->|Three| F[fa:fa-car Car]
"""
_render_mermaid(flow_chart_3)

class_diagram = """
classDiagram
    Animal <|-- Duck
    Animal <|-- Fish
    Animal <|-- Zebra
    Animal : +int age
    Animal : +String gender
    Animal: +isMammal()
    Animal: +mate()
    class Duck{
      +String beakColor
      +swim()
      +quack()
    }
    class Fish{
      -int sizeInFeet
      -canEat()
    }
    class Zebra{
      +bool is_wild
      +run()
    }
"""
_render_mermaid(class_diagram)


state_diagram = """
stateDiagram-v2
    [*] --> Still
    Still --> [*]
    Still --> Moving
    Moving --> Still
    Moving --> Crash
    Crash --> [*]
"""
_render_mermaid(state_diagram)

entity_relation_diagram = """
erDiagram
    CUSTOMER }|..|{ DELIVERY-ADDRESS : has
    CUSTOMER ||--o{ ORDER : places
    CUSTOMER ||--o{ INVOICE : "liable for"
    DELIVERY-ADDRESS ||--o{ ORDER : receives
    INVOICE ||--|{ ORDER : covers
    ORDER ||--|{ ORDER-ITEM : includes
    PRODUCT-CATEGORY ||--|{ PRODUCT : contains
    PRODUCT ||--o{ ORDER-ITEM : "ordered in"
"""
_render_mermaid(entity_relation_diagram)

gantt_chart = """
gantt
    title A Gantt Diagram
    dateFormat  YYYY-MM-DD
    section Section
    A task           :a1, 2014-01-01, 30d
    Another task     :after a1  , 20d
    section Another
    Task in sec      :2014-01-12  , 12d
    another task      : 24d
"""
_render_mermaid(gantt_chart)

user_journey = """
journey
    title My working day
    section Go to work
      Make tea: 5: Me
      Go upstairs: 3: Me
      Do work: 1: Me, Cat
    section Go home
      Go downstairs: 5: Me
      Sit down: 3: Me
"""
_render_mermaid(user_journey)

git_diagram = """
gitGraph
    commit
    commit
    branch develop
    checkout develop
    commit
    commit
    checkout main
    merge develop
    commit
    commit
"""
_render_mermaid(user_journey)

pie_chart = """
pie title Pets adopted by volunteers
    "Dogs" : 386
    "Cats" : 85
    "Rats" : 15
"""
_render_mermaid(pie_chart)

mind_map = """
mindmap
  root((mindmap))
    Origins
      Long history
      ::icon(fa fa-book)
      Popularisation
        British popular psychology author Tony Buzan
    Research
      On effectivness<br/>and features
      On Automatic creation
        Uses
            Creative techniques
            Strategic planning
            Argument mapping
    Tools
      Pen and paper
      Mermaid
"""
_render_mermaid(mind_map)


quadrant_chart = """
quadrantChart
    title Reach and engagement of campaigns
    x-axis Low Reach --> High Reach
    y-axis Low Engagement --> High Engagement
    quadrant-1 We should expand
    quadrant-2 Need to promote
    quadrant-3 Re-evaluate
    quadrant-4 May be improved
    Campaign A: [0.3, 0.6]
    Campaign B: [0.45, 0.23]
    Campaign C: [0.57, 0.69]
    Campaign D: [0.78, 0.34]
    Campaign E: [0.40, 0.34]
    Campaign F: [0.35, 0.78]
"""
_render_mermaid(quadrant_chart)


###################
ui.run()