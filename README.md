# Web GUI

Eine Web User Interface (Web UI) ist die Schnittstelle, die es Benutzern ermöglicht, mit einer Webanwendung oder Website zu interagieren. Sie besteht aus verschiedenen Elementen wie Schaltflächen, Textfeldern, Menüs und anderen grafischen Komponenten, die Benutzereingaben akzeptieren und Informationen darstellen.

In Python gibt es mehrere Frameworks und Bibliotheken, mit denen Entwickler Web UIs erstellen können. Hier sind einige der bekanntesten:

1. **Django** ist ein umfassendes Webframework für Python, das eine eingebaute Unterstützung für die Erstellung von Webanwendungen bietet. Es enthält ein eigenes Template-System für die Erstellung von Web UIs und ermöglicht die Verwendung von Python-Code, um die Benutzeroberfläche zu gestalten und zu verwalten. Django bietet auch Sicherheitsfunktionen und eine ORM (Object-Relational Mapping)-Schicht zur Datenbankinteraktion.
2. **Flask** ist ein leichtgewichtiges Webframework für Python, das Entwicklern die Freiheit gibt, ihre Web UIs nach ihren eigenen Vorstellungen zu gestalten. Flask ist nicht so umfangreich wie Django, bietet jedoch die Flexibilität, verschiedene Bibliotheken und Technologien für die Gestaltung von Web UIs zu verwenden.
3. **FastAPI** ist ein modernes Webframework, das auf schnelle Entwicklung und einfache Handhabung von APIs abzielt. Es eignet sich gut für die Erstellung von RESTful APIs, aber Sie können auch Web UIs mit Template-Engines wie Jinja2 erstellen, wenn Sie dies wünschen.
4. **Tornado** ist ein Framework für die Erstellung von skalierbaren und nicht blockierenden Webanwendungen. Obwohl es hauptsächlich für Websockets und asynchrone Anwendungen entwickelt wurde, kann es auch zur Erstellung von Web UIs verwendet werden.
5. **Streamlit** hingegen ist eine Bibliothek, die speziell für die einfache Erstellung von interaktiven Web UIs für datengesteuerte Anwendungen entwickelt wurde. Es ist besonders nützlich für Datenanalysen und -visualisierungen.

Wir wollen uns in diesem Lab primär mit Web UI-Frameworks wie Streamlit befassen und weniger mit "vollwertigen" Webframeworks wie Django, Flask, FastAPI oder Tornado, die eher in REST APIs oder vollumfänglichen Webanwendungen ihre Stärken ausspielen können, dafür aber auch mit einiger Komplexität einhergehen. Ferner müssen Sie mit Tools wie Streamlit weniger Einblick in Technologien wie JavaScript, HTML und CSS haben, da Ihnen diese Frameworks viel derartige Komplexität kapseln.

[Streamlit](https://streamlit.io) ist eine Open-Source-Python-Bibliothek, die es Entwicklern ermöglicht, interaktive Webanwendungen und Dashboards für Datenvisualisierung und -analyse zu erstellen, ohne umfangreiche Webentwicklungsfähigkeiten zu benötigen. Mit Streamlit können Sie schnell und einfach datengetriebene Anwendungen erstellen, indem Sie Python-Code verwenden, um Benutzeroberflächen zu erstellen, Daten zu verarbeiten und Visualisierungen zu generieren.

- Mit Streamlit können Entwickler **interaktive Anwendungen** in wenigen Zeilen Python-Code erstellen. Sie müssen sich nicht um HTML, CSS oder JavaScript kümmern, da Streamlit diese Aufgaben für Sie erledigt.
- Streamlit ist besonders gut geeignet, um schnell **Prototypen** von Datenanalysen oder -visualisierungen zu erstellen. Sie können sofort Änderungen vornehmen und sehen, wie sich diese auf Ihre Anwendung auswirken.
- Streamlit unterstützt die Integration von verschiedenen Python-Bibliotheken für **Datenvisualisierungen** wie Matplotlib, Plotly, Altair und Bokeh. Dies ermöglicht es Ihnen, Diagramme und Grafiken in Ihre Anwendungen einzufügen.
- Sie können die üblichen **GUI-Widgets** wie Schieberegler, Auswahllisten und Texteingabefelder verwenden, um Benutzereingaben zu erfassen und die Anwendung interaktiv zu gestalten.
- Sobald Sie Ihre Streamlit-Anwendung erstellt haben, können Sie sie leicht über einen **Webbrowser** nutzen.

Streamlit ist besonders nützlich für Datenwissenschaftler, Ingenieure und Entwickler, die schnell prototypische Datenvisualisierungen oder -analysen erstellen und sie mit anderen teilen möchten. Es bietet eine einfache Möglichkeit, datengesteuerte Anwendungen ohne viel Aufwand in Webentwicklung zu erstellen.

## Einarbeitung in Streamlit

- [Installation](https://docs.streamlit.io/get-started/installation) von Streamlit
- Arbeiten Sie sich in die [Kernkonzepte](https://docs.streamlit.io/get-started/fundamentals/main-concepts) von Streamlit ein
- Arbeiten Sie sich in die [erweiterte Konzepte](https://docs.streamlit.io/get-started/fundamentals/advanced-concepts) wie Caching und Session State in Streamlit ein
- Bringen Sie diese Erkenntnisse in einer stichpunktartigen [Zusammenfassung](https://docs.streamlit.io/get-started/fundamentals/summary) auf den Punkt.

Die Inhalte dieser Punkte werden durch den wöchentlichen Test abgeprüft.

## Entwickeln Sie Ihre erste Streamlit-App

[Uber](https://www.uber.com) ist ein multinationales Technologieunternehmen, das ursprünglich im Jahr 2009 gegründet wurde und seinen Hauptsitz in San Francisco, Kalifornien, hat. Das Unternehmen ist vor allem für seine Ride-Sharing-Plattform und seine On-Demand-Fahrdienste bekannt.

Auf Basis dieser [Daten von Abholungen](https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz) sollen Sie nun im Lab eine **containerisierte** Streamlit-Anwendung erstellen, die Uber "Pickups" auf einer Karte von New York City visualisiert.

Unter einem "Pickup" verstehen wir dabei, dass ein registrierter Uber-Fahrer einen Passagier an einem bestimmten Ort abholt und zu seinem gewünschten Ziel fährt.

![Visualization](visualization.png)

Arbeiten Sie dazu bitte folgendes [Tutorial](https://docs.streamlit.io/get-started/tutorials/create-an-app) durch.