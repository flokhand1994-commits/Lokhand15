#!/usr/bin/env python3
"""Generate a PDF with Dutch verb conjugation tables."""

import os

from fpdf import FPDF

# Data for all 55 Dutch verbs
verbs_data = [
    {
        "verb": "1. aandoen (hebben)",
        "sentences": [
            ("Ik heb mijn jas aangedaan.", "I have put on my coat."),
            ("Zij heeft haar schoenen aangedaan.", "She has put on her shoes."),
            ("We hebben warme kleren aangedaan.", "We have put on warm clothes."),
            ("Hij heeft zijn bril aangedaan.", "He has put on his glasses."),
            ("De kinderen hebben hun pyjama aangedaan.", "The children have put on their pajamas."),
        ]
    },
    {
        "verb": "2. aankomen (zijn)",
        "sentences": [
            ("Ik ben laat aangekomen.", "I arrived late."),
            ("We zijn veilig aangekomen.", "We arrived safely."),
            ("De trein is op tijd aangekomen.", "The train arrived on time."),
            ("Zij is gisteren aangekomen.", "She arrived yesterday."),
            ("Mijn ouders zijn vroeg aangekomen.", "My parents arrived early."),
        ]
    },
    {
        "verb": "3. afwassen (hebben)",
        "sentences": [
            ("Ik heb de borden afgewassen.", "I washed the plates."),
            ("Zij heeft alles afgewassen.", "She washed everything."),
            ("We hebben samen afgewassen.", "We washed up together."),
            ("Hij heeft de glazen afgewassen.", "He washed the glasses."),
            ("De kinderen hebben afgewassen.", "The children washed up."),
        ]
    },
    {
        "verb": "4. bakken (hebben)",
        "sentences": [
            ("Ik heb een cake gebakken.", "I baked a cake."),
            ("Zij heeft brood gebakken.", "She baked bread."),
            ("We hebben koekjes gebakken.", "We baked cookies."),
            ("Hij heeft pizza gebakken.", "He baked pizza."),
            ("Mijn moeder heeft taart gebakken.", "My mother baked a pie."),
        ]
    },
    {
        "verb": "5. beginnen (zijn)",
        "sentences": [
            ("Ik ben vroeg begonnen.", "I started early."),
            ("De les is begonnen.", "The lesson has started."),
            ("We zijn samen begonnen.", "We started together."),
            ("Hij is met werken begonnen.", "He started working."),
            ("Het feest is laat begonnen.", "The party started late."),
        ]
    },
    {
        "verb": "6. begrijpen (hebben)",
        "sentences": [
            ("Ik heb het begrepen.", "I understood it."),
            ("Zij heeft de uitleg begrepen.", "She understood the explanation."),
            ("We hebben alles begrepen.", "We understood everything."),
            ("Hij heeft mij goed begrepen.", "He understood me well."),
            ("De studenten hebben de les begrepen.", "The students understood the lesson."),
        ]
    },
    {
        "verb": "7. bezoeken (hebben)",
        "sentences": [
            ("Ik heb mijn tante bezocht.", "I visited my aunt."),
            ("Zij heeft het museum bezocht.", "She visited the museum."),
            ("We hebben Brussel bezocht.", "We visited Brussels."),
            ("Hij heeft de dokter bezocht.", "He visited the doctor."),
            ("Ze hebben hun vrienden bezocht.", "They visited their friends."),
        ]
    },
    {
        "verb": "8. blijven (zijn)",
        "sentences": [
            ("Ik ben thuis gebleven.", "I stayed at home."),
            ("Zij is rustig gebleven.", "She stayed calm."),
            ("We zijn daar gebleven.", "We stayed there."),
            ("Hij is laat gebleven.", "He stayed late."),
            ("De kinderen zijn binnen gebleven.", "The children stayed inside."),
        ]
    },
    {
        "verb": "9. brengen (hebben)",
        "sentences": [
            ("Ik heb bloemen gebracht.", "I brought flowers."),
            ("Zij heeft het cadeau gebracht.", "She brought the gift."),
            ("We hebben eten gebracht.", "We brought food."),
            ("Hij heeft mij naar huis gebracht.", "He brought me home."),
            ("Ze hebben nieuws gebracht.", "They brought news."),
        ]
    },
    {
        "verb": "10. denken (hebben)",
        "sentences": [
            ("Ik heb eraan gedacht.", "I thought about it."),
            ("Zij heeft hetzelfde gedacht.", "She thought the same."),
            ("We hebben lang gedacht.", "We thought for a long time."),
            ("Hij heeft verkeerd gedacht.", "He thought wrongly."),
            ("Ik heb aan jou gedacht.", "I thought of you."),
        ]
    },
    {
        "verb": "11. doen (hebben)",
        "sentences": [
            ("Ik heb mijn best gedaan.", "I did my best."),
            ("Zij heeft het werk gedaan.", "She did the work."),
            ("We hebben alles gedaan.", "We did everything."),
            ("Hij heeft niets gedaan.", "He did nothing."),
            ("Ze hebben veel gedaan.", "They did a lot."),
        ]
    },
    {
        "verb": "12. dragen (hebben)",
        "sentences": [
            ("Ik heb een jurk gedragen.", "I wore a dress."),
            ("Zij heeft een jas gedragen.", "She wore a coat."),
            ("We hebben dezelfde kleren gedragen.", "We wore the same clothes."),
            ("Hij heeft een bril gedragen.", "He wore glasses."),
            ("De acteur heeft een uniform gedragen.", "The actor wore a uniform."),
        ]
    },
    {
        "verb": "13. drinken (hebben)",
        "sentences": [
            ("Ik heb water gedronken.", "I drank water."),
            ("Zij heeft koffie gedronken.", "She drank coffee."),
            ("We hebben wijn gedronken.", "We drank wine."),
            ("Hij heeft thee gedronken.", "He drank tea."),
            ("Ze hebben samen gedronken.", "They drank together."),
        ]
    },
    {
        "verb": "14. eten (hebben)",
        "sentences": [
            ("Ik heb pasta gegeten.", "I ate pasta."),
            ("Zij heeft fruit gegeten.", "She ate fruit."),
            ("We hebben samen gegeten.", "We ate together."),
            ("Hij heeft te veel gegeten.", "He ate too much."),
            ("De kinderen hebben pizza gegeten.", "The children ate pizza."),
        ]
    },
    {
        "verb": "15. gaan (zijn)",
        "sentences": [
            ("Ik ben naar huis gegaan.", "I went home."),
            ("Zij is naar school gegaan.", "She went to school."),
            ("We zijn samen gegaan.", "We went together."),
            ("Hij is vroeg gegaan.", "He left early."),
            ("Ze zijn op vakantie gegaan.", "They went on vacation."),
        ]
    },
    {
        "verb": "16. geven (hebben)",
        "sentences": [
            ("Ik heb een cadeau gegeven.", "I gave a gift."),
            ("Zij heeft advies gegeven.", "She gave advice."),
            ("We hebben hulp gegeven.", "We gave help."),
            ("Hij heeft mij een boek gegeven.", "He gave me a book."),
            ("Ze hebben geld gegeven.", "They gave money."),
        ]
    },
    {
        "verb": "17. hebben (hebben)",
        "sentences": [
            ("Ik heb tijd gehad.", "I had time."),
            ("Zij heeft geluk gehad.", "She was lucky."),
            ("We hebben problemen gehad.", "We had problems."),
            ("Hij heeft honger gehad.", "He was hungry."),
            ("Ze hebben een idee gehad.", "They had an idea."),
        ]
    },
    {
        "verb": "18. helpen (hebben)",
        "sentences": [
            ("Ik heb haar geholpen.", "I helped her."),
            ("Zij heeft mij geholpen.", "She helped me."),
            ("We hebben elkaar geholpen.", "We helped each other."),
            ("Hij heeft de buren geholpen.", "He helped the neighbors."),
            ("Ze hebben samen geholpen.", "They helped together."),
        ]
    },
    {
        "verb": "19. kiezen (hebben)",
        "sentences": [
            ("Ik heb dit gekozen.", "I chose this."),
            ("Zij heeft een jurk gekozen.", "She chose a dress."),
            ("We hebben een film gekozen.", "We chose a movie."),
            ("Hij heeft verkeerd gekozen.", "He chose wrongly."),
            ("Ze hebben snel gekozen.", "They chose quickly."),
        ]
    },
    {
        "verb": "20. kijken (naar) (hebben)",
        "sentences": [
            ("Ik heb naar de film gekeken.", "I watched the movie."),
            ("Zij heeft naar mij gekeken.", "She looked at me."),
            ("We hebben samen gekeken.", "We watched together."),
            ("Hij heeft naar buiten gekeken.", "He looked outside."),
            ("Ze hebben televisie gekeken.", "They watched television."),
        ]
    },
    {
        "verb": "21. komen (zijn)",
        "sentences": [
            ("Ik ben thuis gekomen.", "I came home."),
            ("Zij is laat gekomen.", "She came late."),
            ("We zijn samen gekomen.", "We came together."),
            ("Hij is net gekomen.", "He just came."),
            ("De gasten zijn gekomen.", "The guests came."),
        ]
    },
    {
        "verb": "22. kopen (hebben)",
        "sentences": [
            ("Ik heb een boek gekocht.", "I bought a book."),
            ("Zij heeft schoenen gekocht.", "She bought shoes."),
            ("We hebben eten gekocht.", "We bought food."),
            ("Hij heeft een auto gekocht.", "He bought a car."),
            ("Ze hebben cadeaus gekocht.", "They bought gifts."),
        ]
    },
    {
        "verb": "23. krijgen (hebben)",
        "sentences": [
            ("Ik heb hulp gekregen.", "I received help."),
            ("Zij heeft een brief gekregen.", "She received a letter."),
            ("We hebben geld gekregen.", "We got money."),
            ("Hij heeft koorts gekregen.", "He got a fever."),
            ("Ze hebben toestemming gekregen.", "They got permission."),
        ]
    },
    {
        "verb": "24. lezen (hebben)",
        "sentences": [
            ("Ik heb een boek gelezen.", "I read a book."),
            ("Zij heeft de krant gelezen.", "She read the newspaper."),
            ("We hebben alles gelezen.", "We read everything."),
            ("Hij heeft hardop gelezen.", "He read aloud."),
            ("Ze hebben samen gelezen.", "They read together."),
        ]
    },
    {
        "verb": "25. liggen (hebben)",
        "sentences": [
            ("Het boek heeft op tafel gelegen.", "The book lay on the table."),
            ("Ik heb in bed gelegen.", "I lay in bed."),
            ("Zij heeft op het strand gelegen.", "She lay on the beach."),
            ("We hebben daar lang gelegen.", "We lay there for a long time."),
            ("De sleutel heeft hier gelegen.", "The key was lying here."),
        ]
    },
    {
        "verb": "26. lopen (hebben / zijn)",
        "sentences": [
            ("Ik heb veel gelopen.", "I walked a lot."),
            ("Zij heeft snel gelopen.", "She walked fast."),
            ("We zijn naar huis gelopen.", "We walked home."),
            ("Hij is naar school gelopen.", "He walked to school."),
            ("Ze hebben samen gelopen.", "They walked together."),
        ]
    },
    {
        "verb": "27. nemen (hebben)",
        "sentences": [
            ("Ik heb een besluit genomen.", "I made a decision."),
            ("Zij heeft de bus genomen.", "She took the bus."),
            ("We hebben pauze genomen.", "We took a break."),
            ("Hij heeft mijn plaats genomen.", "He took my place."),
            ("Ze hebben foto's genomen.", "They took photos."),
        ]
    },
    {
        "verb": "28. ontbijten (hebben)",
        "sentences": [
            ("Ik heb vroeg ontbeten.", "I had breakfast early."),
            ("Zij heeft goed ontbeten.", "She had a good breakfast."),
            ("We hebben samen ontbeten.", "We had breakfast together."),
            ("Hij heeft thuis ontbeten.", "He had breakfast at home."),
            ("Ze hebben snel ontbeten.", "They had breakfast quickly."),
        ]
    },
    {
        "verb": "29. opstaan (zijn)",
        "sentences": [
            ("Ik ben vroeg opgestaan.", "I got up early."),
            ("Zij is laat opgestaan.", "She got up late."),
            ("We zijn tegelijk opgestaan.", "We got up at the same time."),
            ("Hij is boos opgestaan.", "He got up angry."),
            ("De kinderen zijn vroeg opgestaan.", "The children got up early."),
        ]
    },
    {
        "verb": "30. rijden (hebben / zijn)",
        "sentences": [
            ("Ik heb snel gereden.", "I drove fast."),
            ("Zij heeft voorzichtig gereden.", "She drove carefully."),
            ("We zijn naar Brussel gereden.", "We drove to Brussels."),
            ("Hij is naar huis gereden.", "He drove home."),
            ("Ze hebben samen gereden.", "They drove together."),
        ]
    },
    {
        "verb": "31. roepen (hebben)",
        "sentences": [
            ("Ik heb zijn naam geroepen.", "I called his name."),
            ("Zij heeft hard geroepen.", "She shouted loudly."),
            ("We hebben om hulp geroepen.", "We called for help."),
            ("Hij heeft mij geroepen.", "He called me."),
            ("Ze hebben samen geroepen.", "They shouted together."),
        ]
    },
    {
        "verb": "32. scheiden (zijn)",
        "sentences": [
            ("Ze zijn vorig jaar gescheiden.", "They divorced last year."),
            ("Mijn ouders zijn gescheiden.", "My parents are divorced."),
            ("Het koppel is gescheiden.", "The couple separated."),
            ("Ze zijn officieel gescheiden.", "They are officially divorced."),
            ("Vrienden zijn gescheiden.", "Friends separated."),
        ]
    },
    {
        "verb": "33. schrijven (hebben)",
        "sentences": [
            ("Ik heb een brief geschreven.", "I wrote a letter."),
            ("Zij heeft een e-mail geschreven.", "She wrote an email."),
            ("We hebben samen geschreven.", "We wrote together."),
            ("Hij heeft een boek geschreven.", "He wrote a book."),
            ("Ze hebben veel geschreven.", "They wrote a lot."),
        ]
    },
    {
        "verb": "34. slapen (hebben)",
        "sentences": [
            ("Ik heb goed geslapen.", "I slept well."),
            ("Zij heeft slecht geslapen.", "She slept badly."),
            ("We hebben lang geslapen.", "We slept long."),
            ("Hij heeft diep geslapen.", "He slept deeply."),
            ("De baby heeft rustig geslapen.", "The baby slept calmly."),
        ]
    },
    {
        "verb": "35. sluiten (hebben)",
        "sentences": [
            ("Ik heb de deur gesloten.", "I closed the door."),
            ("Zij heeft de winkel gesloten.", "She closed the shop."),
            ("We hebben alles gesloten.", "We closed everything."),
            ("Hij heeft het raam gesloten.", "He closed the window."),
            ("Ze hebben vroeg gesloten.", "They closed early."),
        ]
    },
    {
        "verb": "36. snijden (hebben)",
        "sentences": [
            ("Ik heb brood gesneden.", "I cut bread."),
            ("Zij heeft groenten gesneden.", "She cut vegetables."),
            ("We hebben kaas gesneden.", "We cut cheese."),
            ("Hij heeft zich gesneden.", "He cut himself."),
            ("Ze hebben alles gesneden.", "They cut everything."),
        ]
    },
    {
        "verb": "37. spreken (hebben)",
        "sentences": [
            ("Ik heb Nederlands gesproken.", "I spoke Dutch."),
            ("Zij heeft met mij gesproken.", "She spoke with me."),
            ("We hebben lang gesproken.", "We talked for a long time."),
            ("Hij heeft duidelijk gesproken.", "He spoke clearly."),
            ("Ze hebben samen gesproken.", "They spoke together."),
        ]
    },
    {
        "verb": "38. strijken (hebben)",
        "sentences": [
            ("Ik heb mijn kleren gestreken.", "I ironed my clothes."),
            ("Zij heeft de blouse gestreken.", "She ironed the blouse."),
            ("We hebben alles gestreken.", "We ironed everything."),
            ("Hij heeft het overhemd gestreken.", "He ironed the shirt."),
            ("Ze hebben samen gestreken.", "They ironed together."),
        ]
    },
    {
        "verb": "39. uitdoen (hebben)",
        "sentences": [
            ("Ik heb mijn jas uitgedaan.", "I took off my coat."),
            ("Zij heeft haar schoenen uitgedaan.", "She took off her shoes."),
            ("We hebben het licht uitgedaan.", "We turned off the light."),
            ("Hij heeft zijn bril uitgedaan.", "He took off his glasses."),
            ("De kinderen hebben hun jassen uitgedaan.", "The children took off their coats."),
        ]
    },
    {
        "verb": "40. vallen (zijn)",
        "sentences": [
            ("Ik ben gevallen.", "I fell."),
            ("Zij is van de trap gevallen.", "She fell down the stairs."),
            ("We zijn niet gevallen.", "We did not fall."),
            ("Hij is hard gevallen.", "He fell hard."),
            ("Het kind is gevallen.", "The child fell."),
        ]
    },
    {
        "verb": "41. vergeten (hebben / zijn)",
        "sentences": [
            ("Ik heb mijn sleutels vergeten.", "I forgot my keys."),
            ("Zij heeft de afspraak vergeten.", "She forgot the appointment."),
            ("We hebben het adres vergeten.", "We forgot the address."),
            ("Hij is mij vergeten.", "He forgot me."),
            ("Ze zijn dat idee vergeten.", "They forgot that idea."),
        ]
    },
    {
        "verb": "42. verkopen (hebben)",
        "sentences": [
            ("Ik heb mijn auto verkocht.", "I sold my car."),
            ("Zij heeft het huis verkocht.", "She sold the house."),
            ("We hebben alles verkocht.", "We sold everything."),
            ("Hij heeft brood verkocht.", "He sold bread."),
            ("Ze hebben snel verkocht.", "They sold quickly."),
        ]
    },
    {
        "verb": "43. verliezen (hebben)",
        "sentences": [
            ("Ik heb mijn sleutel verloren.", "I lost my key."),
            ("Zij heeft haar baan verloren.", "She lost her job."),
            ("We hebben de wedstrijd verloren.", "We lost the match."),
            ("Hij heeft geld verloren.", "He lost money."),
            ("Ze hebben alles verloren.", "They lost everything."),
        ]
    },
    {
        "verb": "44. vertrekken (zijn)",
        "sentences": [
            ("Ik ben vroeg vertrokken.", "I left early."),
            ("Zij is gisteren vertrokken.", "She left yesterday."),
            ("We zijn samen vertrokken.", "We left together."),
            ("Hij is naar huis vertrokken.", "He left for home."),
            ("De trein is vertrokken.", "The train departed."),
        ]
    },
    {
        "verb": "45. vinden (hebben)",
        "sentences": [
            ("Ik heb het leuk gevonden.", "I liked it."),
            ("Zij heeft een oplossing gevonden.", "She found a solution."),
            ("We hebben het moeilijk gevonden.", "We found it difficult."),
            ("Hij heeft zijn bril gevonden.", "He found his glasses."),
            ("Ze hebben elkaar gevonden.", "They found each other."),
        ]
    },
    {
        "verb": "46. wassen (hebben)",
        "sentences": [
            ("Ik heb mijn handen gewassen.", "I washed my hands."),
            ("Zij heeft de kleren gewassen.", "She washed the clothes."),
            ("We hebben alles gewassen.", "We washed everything."),
            ("Hij heeft zijn auto gewassen.", "He washed his car."),
            ("Ze hebben samen gewassen.", "They washed together."),
        ]
    },
    {
        "verb": "47. weten (hebben)",
        "sentences": [
            ("Ik heb dat niet geweten.", "I did not know that."),
            ("Zij heeft het altijd geweten.", "She always knew it."),
            ("We hebben het nu geweten.", "We knew it then."),
            ("Hij heeft het antwoord geweten.", "He knew the answer."),
            ("Ze hebben niets geweten.", "They knew nothing."),
        ]
    },
    {
        "verb": "48. winnen (hebben)",
        "sentences": [
            ("Ik heb de prijs gewonnen.", "I won the prize."),
            ("Zij heeft de wedstrijd gewonnen.", "She won the match."),
            ("We hebben samen gewonnen.", "We won together."),
            ("Hij heeft veel geld gewonnen.", "He won a lot of money."),
            ("Ze hebben alles gewonnen.", "They won everything."),
        ]
    },
    {
        "verb": "49. worden (zijn)",
        "sentences": [
            ("Ik ben moe geworden.", "I became tired."),
            ("Zij is boos geworden.", "She got angry."),
            ("We zijn vrienden geworden.", "We became friends."),
            ("Hij is ouder geworden.", "He became older."),
            ("Ze zijn beroemd geworden.", "They became famous."),
        ]
    },
    {
        "verb": "50. zien (hebben)",
        "sentences": [
            ("Ik heb haar gezien.", "I saw her."),
            ("Zij heeft de film gezien.", "She saw the movie."),
            ("We hebben alles gezien.", "We saw everything."),
            ("Hij heeft niets gezien.", "He saw nothing."),
            ("Ze hebben elkaar gezien.", "They saw each other."),
        ]
    },
    {
        "verb": "51. zijn (zijn)",
        "sentences": [
            ("Ik ben daar geweest.", "I have been there."),
            ("Zij is ziek geweest.", "She was ill."),
            ("We zijn thuis geweest.", "We were at home."),
            ("Hij is bang geweest.", "He was afraid."),
            ("Ze zijn samen geweest.", "They were together."),
        ]
    },
    {
        "verb": "52. zingen (hebben)",
        "sentences": [
            ("Ik heb een lied gezongen.", "I sang a song."),
            ("Zij heeft mooi gezongen.", "She sang beautifully."),
            ("We hebben samen gezongen.", "We sang together."),
            ("Hij heeft hard gezongen.", "He sang loudly."),
            ("Ze hebben lang gezongen.", "They sang for a long time."),
        ]
    },
    {
        "verb": "53. zitten (hebben)",
        "sentences": [
            ("Ik heb hier gezeten.", "I sat here."),
            ("Zij heeft lang gezeten.", "She sat for a long time."),
            ("We hebben samen gezeten.", "We sat together."),
            ("Hij heeft naast mij gezeten.", "He sat next to me."),
            ("Ze hebben binnen gezeten.", "They sat inside."),
        ]
    },
    {
        "verb": "54. zoeken (hebben)",
        "sentences": [
            ("Ik heb mijn sleutel gezocht.", "I looked for my key."),
            ("Zij heeft werk gezocht.", "She looked for a job."),
            ("We hebben een oplossing gezocht.", "We looked for a solution."),
            ("Hij heeft hulp gezocht.", "He sought help."),
            ("Ze hebben lang gezocht.", "They searched for a long time."),
        ]
    },
    {
        "verb": "55. zwemmen (hebben)",
        "sentences": [
            ("Ik heb gezwommen.", "I swam."),
            ("Zij heeft in zee gezwommen.", "She swam in the sea."),
            ("We hebben samen gezwommen.", "We swam together."),
            ("Hij heeft snel gezwommen.", "He swam fast."),
            ("De kinderen hebben gezwommen.", "The children swam."),
        ]
    },
]


class DutchVerbsPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(40, 80, 120)
        self.cell(0, 10, 'Dutch Verbs - Perfect Tense (Voltooid Tegenwoordige Tijd)', 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def add_verb_table(self, verb_data):
        verb_name = verb_data["verb"]
        sentences = verb_data["sentences"]
        
        # Check if we need a new page (estimate table height)
        table_height = 8 + (len(sentences) * 8) + 10  # header + rows + spacing
        if self.get_y() + table_height > 270:
            self.add_page()
        
        # Verb title
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(50, 50, 50)
        self.set_fill_color(220, 235, 250)
        self.cell(0, 8, verb_name, 0, 1, 'L', fill=True)
        
        # Table header
        self.set_font('Helvetica', 'B', 9)
        self.set_fill_color(70, 130, 180)
        self.set_text_color(255, 255, 255)
        self.cell(95, 7, 'Dutch Sentence', 1, 0, 'C', fill=True)
        self.cell(95, 7, 'English Translation', 1, 1, 'C', fill=True)
        
        # Table rows
        self.set_font('Helvetica', '', 9)
        self.set_text_color(40, 40, 40)
        
        for i, (dutch, english) in enumerate(sentences):
            if i % 2 == 0:
                self.set_fill_color(245, 250, 255)
            else:
                self.set_fill_color(255, 255, 255)
            
            self.cell(95, 7, dutch, 1, 0, 'L', fill=True)
            self.cell(95, 7, english, 1, 1, 'L', fill=True)
        
        self.ln(5)


def create_pdf():
    pdf = DutchVerbsPDF()
    pdf.add_page()
    
    for verb_data in verbs_data:
        pdf.add_verb_table(verb_data)
    
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dutch_verbs.pdf")
    pdf.output(output_path)
    print(f"PDF created successfully: {output_path}")
    return output_path


if __name__ == "__main__":
    create_pdf()
