from nicegui import ui

from typing import Callable, Literal, Optional, Union
WindowType = Literal['python', 'bash', 'browser']
WINDOW_BG_COLORS = {
    'python': ('#eef5fb', '#2b323b'),
    'bash': ('#e8e8e8', '#2b323b'),
    'browser': ('#ffffff', '#181c21'),
}

def _init_cap(s):
    return " ".join([i.strip().capitalize() for i in s.split("_") if i.strip()])

def _get_var_name(v):
    for name in globals():
        x = eval(name)
        if x is not None and x == v:
            return name
    return ""

def _dots() -> None:
    with ui.row().classes('gap-1 relative left-[1px] top-[1px]'):
        ui.icon('circle').classes('text-[13px] text-red-400')
        ui.icon('circle').classes('text-[13px] text-yellow-400')
        ui.icon('circle').classes('text-[13px] text-green-400')

def window(type: WindowType, *, title: str = '', tab: Union[str, Callable] = '', classes: str = '') -> ui.column:
    bar_color = ('#00000010', '#ffffff10')
    color = WINDOW_BG_COLORS[type]
    with ui.card().classes(f'no-wrap bg-[{color[0]}] dark:bg-[{color[1]}] rounded-xl p-0 gap-0 {classes}') \
            .style('box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1)'):
        with ui.row().classes(f'w-full h-8 p-2 bg-[{bar_color[0]}] dark:bg-[{bar_color[1]}]'):
            _dots()
            if title:
                ui.label(title) \
                    .classes('text-sm text-gray-600 dark:text-gray-400 absolute left-1/2 top-[6px]') \
                    .style('transform: translateX(-50%)')
            if tab:
                with ui.row().classes('gap-0'):
                    with ui.label().classes(f'w-2 h-[24px] bg-[{color[0]}] dark:bg-[{color[1]}]'):
                        ui.label().classes(
                            f'w-full h-full bg-[{bar_color[0]}] dark:bg-[{bar_color[1]}] rounded-br-[6px]')
                    with ui.row().classes(f'text-sm text-gray-600 dark:text-gray-400 px-6 py-1 h-[24px] rounded-t-[6px] bg-[{color[0]}] dark:bg-[{color[1]}] items-center gap-2'):
                        tab() if callable(tab) else ui.label(tab)
                    with ui.label().classes(f'w-2 h-[24px] bg-[{color[0]}] dark:bg-[{color[1]}]'):
                        ui.label().classes(
                            f'w-full h-full bg-[{bar_color[0]}] dark:bg-[{bar_color[1]}] rounded-bl-[6px]')
        return ui.column().classes('w-full h-full overflow-auto')

def python_window(title: Optional[str] = None, *, classes: str = '') -> ui.card:
    return window('python', title=title or 'main.py', classes=classes).classes('p-2 python-window')

def _render_mermaid(src_code):
    with ui.column():
        ui.label(_init_cap(_get_var_name(src_code))).style('color: blue; font-size: 140%; font-weight: 300')
        ui.mermaid(src_code)
        with ui.expansion('Show code', icon='info'):   # apple
            with python_window(classes='w-full max-w-[44rem]'):
                ui.markdown(f'````python\n{src_code}\n````')


ui.markdown(""" ## Mermaid - A Nice Diagramming Tool
    - [Home](https://mermaid.js.org/)
    - [Live Editor](https://mermaid.live/edit)
    - [Docs](https://mermaid.js.org/intro/)
    - [Github](https://github.com/mermaid-js/mermaid)
                        
""")

ui.markdown(""" ### Basic""")
left_to_right_graph = """
    graph LR;
        A --> B;
        A --> C;
"""
_render_mermaid(left_to_right_graph)

top_down_graph = '''
    graph TD;
        女 --> 好;
        子 --> 好;
        好 --> 好人;
        好 --> 好事;
        好 --> 好地方;
        style 好人 fill:pink
        style 好事 fill:lightgreen
        style 好地方 fill:lightblue
'''

_render_mermaid(top_down_graph)


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
_render_mermaid(flowchart_1)

flowchart_2 = '''
        flowchart TD
            A[Start] --> B{Is it?}
            B -->|Yes| C[OK]
            C --> D[Rethink]
            D --> B
            B ---->|No| E[End]
    '''
_render_mermaid(flowchart_2)

flow_chart_3 = """
flowchart TD
    A[Christmas] -->|Get money| B(Go shopping)
    B --> C{Let me think}
    C -->|One| D[Laptop]
    C -->|Two| E[iPhone]
    C -->|Three| F[fa:fa-car Car]
"""
_render_mermaid(flow_chart_3)

## %%{init: {"flowchart": {"htmlLabels": true}} }%%
flowchart_with_link = '''
graph TD; 
  A(Up)-->B(See NiceGui)-->C(Enjoy);
  click B "https://nicegui.io/documentation#mermaid_diagrams"
  style B fill:lightblue
'''

_render_mermaid(flowchart_with_link)


ui.markdown(""" ### More [Examples](https://mermaid.js.org/intro/)
           
""")

seq_diagram = """
sequenceDiagram
    Alice->>+John: Hello John, how are you?
    Alice->>+John: John, can you hear me?
    John-->>-Alice: Hi Alice, I can hear you!
    John-->>-Alice: I feel great!
"""
_render_mermaid(seq_diagram)


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
_render_mermaid(git_diagram)

pie_chart = """
pie title Pets adopted by volunteers
    "Dogs" : 386
    "Cats" : 200
    "Rats" : 100
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
      Mermaid(http://mermaid.js.org)
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