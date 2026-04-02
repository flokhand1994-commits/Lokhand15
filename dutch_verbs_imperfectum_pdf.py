#!/usr/bin/env python3
"""Generate a PDF: 50 common Dutch verbs in the imperfect (onvoltooid verleden tijd)."""

import os

from fpdf import FPDF

# 25 high-frequency irregular + 25 regular verbs (weak -te/-de), example sentences in OVT
verbs_data = [
    # --- Irregular (strong, suppletive, modals) ---
    {
        "verb": "1. zijn (onregelmatig)",
        "sentences": [
            ("Ik was gisteren ziek.", "I was ill yesterday."),
            ("Jij was daar al eerder.", "You had been there before."),
            ("Hij was heel rustig.", "He was very calm."),
            ("We waren samen op vakantie.", "We were on holiday together."),
            ("Zij waren nog niet klaar.", "They were not ready yet."),
        ],
    },
    {
        "verb": "2. hebben (onregelmatig)",
        "sentences": [
            ("Ik had geen tijd.", "I had no time."),
            ("Jij had gelijk.", "You were right."),
            ("Hij had een nieuwe fiets.", "He had a new bicycle."),
            ("We hadden honger.", "We were hungry."),
            ("Zij hadden veel vragen.", "They had many questions."),
        ],
    },
    {
        "verb": "3. gaan (onregelmatig)",
        "sentences": [
            ("Ik ging elke dag naar school.", "I went to school every day."),
            ("Jij ging te laat naar bed.", "You went to bed too late."),
            ("Hij ging alleen naar de winkel.", "He went to the shop alone."),
            ("We gingen vaak naar het park.", "We often went to the park."),
            ("Zij gingen samen naar huis.", "They went home together."),
        ],
    },
    {
        "verb": "4. komen (onregelmatig)",
        "sentences": [
            ("Ik kwam uit Amsterdam.", "I came from Amsterdam."),
            ("Jij kwam op tijd.", "You came on time."),
            ("Hij kwam met de trein.", "He came by train."),
            ("We kwamen elkaar tegen.", "We ran into each other."),
            ("Zij kwamen gisteren langs.", "They came by yesterday."),
        ],
    },
    {
        "verb": "5. zien (onregelmatig)",
        "sentences": [
            ("Ik zag een mooie regenboog.", "I saw a beautiful rainbow."),
            ("Jij zag het probleem meteen.", "You saw the problem immediately."),
            ("Hij zag er moe uit.", "He looked tired."),
            ("We zagen weinig mensen.", "We saw few people."),
            ("Zij zagen de film al.", "They had already seen the film."),
        ],
    },
    {
        "verb": "6. doen (onregelmatig)",
        "sentences": [
            ("Ik deed mijn best op school.", "I did my best at school."),
            ("Jij deed precies wat ik zei.", "You did exactly what I said."),
            ("Hij deed niets de hele dag.", "He did nothing all day."),
            ("We deden het samen.", "We did it together."),
            ("Zij deden moeilijk over alles.", "They made a fuss about everything."),
        ],
    },
    {
        "verb": "7. zeggen (onregelmatig)",
        "sentences": [
            ("Ik zei de waarheid.", "I told the truth."),
            ("Jij zei niets.", "You said nothing."),
            ("Hij zei dat het goed was.", "He said it was fine."),
            ("We zeiden het nog een keer.", "We said it again."),
            ("Zij zeiden ja tegen het plan.", "They said yes to the plan."),
        ],
    },
    {
        "verb": "8. geven (onregelmatig)",
        "sentences": [
            ("Ik gaf haar een cadeau.", "I gave her a present."),
            ("Jij gaf goed advies.", "You gave good advice."),
            ("Hij gaf les op die school.", "He taught at that school."),
            ("We gaven geld aan het goede doel.", "We gave money to charity."),
            ("Zij gaven een feestje.", "They threw a little party."),
        ],
    },
    {
        "verb": "9. nemen (onregelmatig)",
        "sentences": [
            ("Ik nam de bus naar werk.", "I took the bus to work."),
            ("Jij nam de verkeerde afslag.", "You took the wrong exit."),
            ("Hij nam rustig de tijd.", "He took his time."),
            ("We namen een taxi.", "We took a taxi."),
            ("Zij namen hun jassen mee.", "They took their coats with them."),
        ],
    },
    {
        "verb": "10. staan (onregelmatig)",
        "sentences": [
            ("Ik stond een uur in de rij.", "I stood in line for an hour."),
            ("Jij stond voor de deur.", "You stood in front of the door."),
            ("Hij stond vroeg op.", "He got up early."),
            ("We stonden op het perron.", "We stood on the platform."),
            ("Zij stonden klaar om te vertrekken.", "They were ready to leave."),
        ],
    },
    {
        "verb": "11. liggen (onregelmatig)",
        "sentences": [
            ("Ik lag nog in bed.", "I was still in bed."),
            ("Jij lag op de bank.", "You lay on the sofa."),
            ("Het boek lag op tafel.", "The book lay on the table."),
            ("We lagen in de zon.", "We lay in the sun."),
            ("De sleutels lagen in de la.", "The keys lay in the drawer."),
        ],
    },
    {
        "verb": "12. zitten (onregelmatig)",
        "sentences": [
            ("Ik zat naast het raam.", "I sat next to the window."),
            ("Jij zat goed in je werk.", "You were doing well at your job."),
            ("Hij zat uren op zijn kamer.", "He sat in his room for hours."),
            ("We zaten in het restaurant.", "We sat in the restaurant."),
            ("Zij zaten te wachten.", "They were waiting."),
        ],
    },
    {
        "verb": "13. brengen (onregelmatig)",
        "sentences": [
            ("Ik bracht de kinderen naar school.", "I brought the children to school."),
            ("Jij bracht nieuws van huis.", "You brought news from home."),
            ("Hij bracht koffie mee.", "He brought coffee along."),
            ("We brachten een bezoek aan oma.", "We paid grandma a visit."),
            ("Zij brachten bloemen mee.", "They brought flowers."),
        ],
    },
    {
        "verb": "14. denken (onregelmatig)",
        "sentences": [
            ("Ik dacht aan jou.", "I thought of you."),
            ("Jij dacht hetzelfde.", "You thought the same."),
            ("Hij dacht lang na.", "He thought for a long time."),
            ("We dachten dat het zou regenen.", "We thought it would rain."),
            ("Zij dachten aan een oplossing.", "They thought of a solution."),
        ],
    },
    {
        "verb": "15. weten (onregelmatig)",
        "sentences": [
            ("Ik wist het antwoord niet.", "I did not know the answer."),
            ("Jij wist van niets.", "You knew nothing about it."),
            ("Hij wist alles van computers.", "He knew everything about computers."),
            ("We wisten niet waar we moesten zijn.", "We did not know where we had to be."),
            ("Zij wisten het pas later.", "They only knew later."),
        ],
    },
    {
        "verb": "16. kunnen (onregelmatig)",
        "sentences": [
            ("Ik kon niet komen.", "I could not come."),
            ("Jij kon goed zwemmen.", "You could swim well."),
            ("Hij kon de deur niet openen.", "He could not open the door."),
            ("We konden elkaar niet horen.", "We could not hear each other."),
            ("Zij konden niet blijven.", "They could not stay."),
        ],
    },
    {
        "verb": "17. moeten (onregelmatig)",
        "sentences": [
            ("Ik moest overwerken.", "I had to work overtime."),
            ("Jij moest wachten.", "You had to wait."),
            ("Hij moest naar de dokter.", "He had to go to the doctor."),
            ("We moesten opschieten.", "We had to hurry."),
            ("Zij moesten vroeg opstaan.", "They had to get up early."),
        ],
    },
    {
        "verb": "18. willen (onregelmatig)",
        "sentences": [
            ("Ik wilde graag helpen.", "I wanted to help."),
            ("Jij wilde niet mee.", "You did not want to come along."),
            ("Hij wilde iets anders worden.", "He wanted to become something else."),
            ("We wilden naar het strand.", "We wanted to go to the beach."),
            ("Zij wilden vertrekken.", "They wanted to leave."),
        ],
    },
    {
        "verb": "19. mogen (onregelmatig)",
        "sentences": [
            ("Ik mocht niet naar buiten.", "I was not allowed to go outside."),
            ("Jij mocht een koekje.", "You were allowed a cookie."),
            ("Hij mocht niet roken.", "He was not allowed to smoke."),
            ("We mochten eerder naar huis.", "We were allowed home earlier."),
            ("Zij mochten blijven slapen.", "They were allowed to stay the night."),
        ],
    },
    {
        "verb": "20. worden (onregelmatig)",
        "sentences": [
            ("Ik werd ouder.", "I grew older."),
            ("Jij werd boos.", "You got angry."),
            ("Hij werd arts.", "He became a doctor."),
            ("We werden vrienden.", "We became friends."),
            ("Zij werden beroemd.", "They became famous."),
        ],
    },
    {
        "verb": "21. blijven (onregelmatig)",
        "sentences": [
            ("Ik bleef thuis.", "I stayed home."),
            ("Jij bleef rustig.", "You stayed calm."),
            ("Hij bleef lang zitten.", "He sat for a long time."),
            ("We bleven in contact.", "We stayed in touch."),
            ("Zij bleven een week langer.", "They stayed a week longer."),
        ],
    },
    {
        "verb": "22. lopen (onregelmatig)",
        "sentences": [
            ("Ik liep elke ochtend hard.", "I ran every morning."),
            ("Jij liep de verkeerde kant op.", "You walked the wrong way."),
            ("Hij liep naar de bus.", "He walked to the bus."),
            ("We liepen door het bos.", "We walked through the forest."),
            ("Zij liepen snel naar huis.", "They walked home quickly."),
        ],
    },
    {
        "verb": "23. vinden (onregelmatig)",
        "sentences": [
            ("Ik vond het leuk.", "I liked it."),
            ("Jij vond de sleutel.", "You found the key."),
            ("Hij vond werk in de stad.", "He found work in the city."),
            ("We vonden het moeilijk.", "We found it difficult."),
            ("Zij vonden geen parkeerplek.", "They found no parking space."),
        ],
    },
    {
        "verb": "24. spreken (onregelmatig)",
        "sentences": [
            ("Ik sprak Nederlands met haar.", "I spoke Dutch with her."),
            ("Jij sprak te zacht.", "You spoke too softly."),
            ("Hij sprak drie talen.", "He spoke three languages."),
            ("We spraken af bij het station.", "We arranged to meet at the station."),
            ("Zij spraken over het weer.", "They spoke about the weather."),
        ],
    },
    {
        "verb": "25. lezen (onregelmatig)",
        "sentences": [
            ("Ik las elke avond een boek.", "I read a book every evening."),
            ("Jij las de krant.", "You read the newspaper."),
            ("Hij las voor aan de kinderen.", "He read aloud to the children."),
            ("We lazen het hele artikel.", "We read the whole article."),
            ("Zij lazen graag strips.", "They liked reading comics."),
        ],
    },
    # --- Regular (zwak: -te / -de) ---
    {
        "verb": "26. werken (regelmatig)",
        "sentences": [
            ("Ik werkte in een ziekenhuis.", "I worked in a hospital."),
            ("Jij werkte tot laat.", "You worked until late."),
            ("Hij werkte parttime.", "He worked part-time."),
            ("We werkten in hetzelfde team.", "We worked on the same team."),
            ("Zij werkten zes dagen per week.", "They worked six days a week."),
        ],
    },
    {
        "verb": "27. maken (regelmatig)",
        "sentences": [
            ("Ik maakte soep.", "I made soup."),
            ("Jij maakte een grap.", "You made a joke."),
            ("Hij maakte zijn huiswerk.", "He did his homework."),
            ("We maakten een wandeling.", "We took a walk."),
            ("Zij maakten veel lawaai.", "They made a lot of noise."),
        ],
    },
    {
        "verb": "28. horen (regelmatig)",
        "sentences": [
            ("Ik hoorde een geluid buiten.", "I heard a sound outside."),
            ("Jij hoorde het nieuws al.", "You had already heard the news."),
            ("Hij hoorde slecht op dat oor.", "He was hard of hearing in that ear."),
            ("We hoorden de bel niet.", "We did not hear the bell."),
            ("Zij hoorden muziek uit de kamer.", "They heard music from the room."),
        ],
    },
    {
        "verb": "29. wonen (regelmatig)",
        "sentences": [
            ("Ik woonde bij mijn ouders.", "I lived with my parents."),
            ("Jij woonde op de bovenste verdieping.", "You lived on the top floor."),
            ("Hij woonde dicht bij school.", "He lived close to school."),
            ("We woonden jaren in Utrecht.", "We lived in Utrecht for years."),
            ("Zij woonden in een flat.", "They lived in a flat."),
        ],
    },
    {
        "verb": "30. leren (regelmatig)",
        "sentences": [
            ("Ik leerde elke dag nieuwe woorden.", "I learned new words every day."),
            ("Jij leerde snel.", "You learned quickly."),
            ("Hij leerde piano spelen.", "He learned to play the piano."),
            ("We leerden elkaar kennen op school.", "We got to know each other at school."),
            ("Zij leerden Frans op de middelbare school.", "They learned French in secondary school."),
        ],
    },
    {
        "verb": "31. spelen (regelmatig)",
        "sentences": [
            ("Ik speelde voetbal op zaterdag.", "I played football on Saturdays."),
            ("Jij speelde het spel eerlijk.", "You played the game fairly."),
            ("Hij speelde gitaar in een band.", "He played guitar in a band."),
            ("We speelden samen in de tuin.", "We played together in the garden."),
            ("Zij speelden een wedstrijd.", "They played a match."),
        ],
    },
    {
        "verb": "32. praten (regelmatig)",
        "sentences": [
            ("Ik praatte met de buurman.", "I talked with the neighbour."),
            ("Jij praatte te veel tijdens de film.", "You talked too much during the film."),
            ("Hij praatte rustig verder.", "He calmly continued talking."),
            ("We praatten uren over politiek.", "We talked for hours about politics."),
            ("Zij praatten niet met elkaar.", "They did not talk to each other."),
        ],
    },
    {
        "verb": "33. hopen (regelmatig)",
        "sentences": [
            ("Ik hoopte op goed weer.", "I hoped for good weather."),
            ("Jij hoopte op een betere baan.", "You hoped for a better job."),
            ("Hij hoopte dat alles goed zou gaan.", "He hoped everything would go well."),
            ("We hoopten op een telefoontje.", "We hoped for a phone call."),
            ("Zij hoopten vroeg thuis te zijn.", "They hoped to be home early."),
        ],
    },
    {
        "verb": "34. bellen (regelmatig)",
        "sentences": [
            ("Ik belde je gisteren.", "I called you yesterday."),
            ("Jij belde naar de receptie.", "You called reception."),
            ("Hij belde de hele tijd.", "He kept calling."),
            ("We belden om een afspraak te maken.", "We called to make an appointment."),
            ("Zij belden elke week.", "They called every week."),
        ],
    },
    {
        "verb": "35. gebruiken (regelmatig)",
        "sentences": [
            ("Ik gebruikte je pen.", "I used your pen."),
            ("Jij gebruikte te veel zout.", "You used too much salt."),
            ("Hij gebruikte de app elke dag.", "He used the app every day."),
            ("We gebruikten het openbaar vervoer.", "We used public transport."),
            ("Zij gebruikten oude kaarten.", "They used old maps."),
        ],
    },
    {
        "verb": "36. studeren (regelmatig)",
        "sentences": [
            ("Ik studeerde medicijnen.", "I studied medicine."),
            ("Jij studeerde tot laat in de bibliotheek.", "You studied late in the library."),
            ("Hij studeerde in Leiden.", "He studied in Leiden."),
            ("We studeerden voor het examen.", "We studied for the exam."),
            ("Zij studeerden samen.", "They studied together."),
        ],
    },
    {
        "verb": "37. antwoorden (regelmatig)",
        "sentences": [
            ("Ik antwoordde op de mail.", "I replied to the email."),
            ("Jij antwoordde niet.", "You did not answer."),
            ("Hij antwoordde kort en duidelijk.", "He answered briefly and clearly."),
            ("We antwoordden op alle vragen.", "We answered all the questions."),
            ("Zij antwoordden met ja of nee.", "They answered with yes or no."),
        ],
    },
    {
        "verb": "38. proberen (regelmatig)",
        "sentences": [
            ("Ik probeerde het opnieuw.", "I tried again."),
            ("Jij probeerde het recept van oma.", "You tried grandma's recipe."),
            ("Hij probeerde te helpen.", "He tried to help."),
            ("We probeerden rustig te blijven.", "We tried to stay calm."),
            ("Zij probeerden de deur open te duwen.", "They tried to push the door open."),
        ],
    },
    {
        "verb": "39. betalen (regelmatig)",
        "sentences": [
            ("Ik betaalde contant.", "I paid in cash."),
            ("Jij betaalde de rekening.", "You paid the bill."),
            ("Hij betaalde te veel voor de taxi.", "He paid too much for the taxi."),
            ("We betaalden de huur op tijd.", "We paid the rent on time."),
            ("Zij betaalden met pin.", "They paid by card."),
        ],
    },
    {
        "verb": "40. wachten (regelmatig)",
        "sentences": [
            ("Ik wachtte op de bus.", "I waited for the bus."),
            ("Jij wachtte in de hal.", "You waited in the hall."),
            ("Hij wachtte een halfuur.", "He waited half an hour."),
            ("We wachtten tot het donker werd.", "We waited until it got dark."),
            ("Zij wachtten op goed nieuws.", "They waited for good news."),
        ],
    },
    {
        "verb": "41. tekenen (regelmatig)",
        "sentences": [
            ("Ik tekende een huis.", "I drew a house."),
            ("Jij tekende elke dag in je schetsboek.", "You drew in your sketchbook every day."),
            ("Hij tekende strips voor de krant.", "He drew comics for the newspaper."),
            ("We tekenden het plan op het bord.", "We drew the plan on the board."),
            ("Zij tekenden portretten.", "They drew portraits."),
        ],
    },
    {
        "verb": "42. dansen (regelmatig)",
        "sentences": [
            ("Ik danste graag op feestjes.", "I liked dancing at parties."),
            ("Jij danste met haar.", "You danced with her."),
            ("Hij danste professioneel.", "He danced professionally."),
            ("We dansten tot middernacht.", "We danced until midnight."),
            ("Zij dansten op de muziek.", "They danced to the music."),
        ],
    },
    {
        "verb": "43. luisteren (regelmatig)",
        "sentences": [
            ("Ik luisterde naar de radio.", "I listened to the radio."),
            ("Jij luisterde goed naar de uitleg.", "You listened carefully to the explanation."),
            ("Hij luisterde naar haar verhaal.", "He listened to her story."),
            ("We luisterden naar een podcast.", "We listened to a podcast."),
            ("Zij luisterden niet naar de leraar.", "They did not listen to the teacher."),
        ],
    },
    {
        "verb": "44. koken (regelmatig)",
        "sentences": [
            ("Ik kookte pasta voor het avondeten.", "I cooked pasta for dinner."),
            ("Jij kookte graag op zondag.", "You liked cooking on Sundays."),
            ("Hij kookte in een restaurant.", "He cooked in a restaurant."),
            ("We kookten samen in de keuken.", "We cooked together in the kitchen."),
            ("Zij kookten traditionele gerechten.", "They cooked traditional dishes."),
        ],
    },
    {
        "verb": "45. passen (regelmatig)",
        "sentences": [
            ("De jas paste perfect.", "The coat fit perfectly."),
            ("De schoenen pasten niet meer.", "The shoes no longer fit."),
            ("Het schema paste bij onze plannen.", "The schedule fitted our plans."),
            ("De kleuren pasten bij elkaar.", "The colours matched each other."),
            ("De sleutel paste niet in het slot.", "The key did not fit in the lock."),
        ],
    },
    {
        "verb": "46. reizen (regelmatig)",
        "sentences": [
            ("Ik reisde veel voor mijn werk.", "I travelled a lot for my work."),
            ("Jij reisde met de trein.", "You travelled by train."),
            ("Hij reisde alleen door Azië.", "He travelled alone through Asia."),
            ("We reisden in de zomervakantie.", "We travelled in the summer holidays."),
            ("Zij reisden met een grote rugzak.", "They travelled with a big backpack."),
        ],
    },
    {
        "verb": "47. baden (regelmatig)",
        "sentences": [
            ("Ik badde in warm water.", "I bathed in warm water."),
            ("Het kind badde in de wastafel.", "The child bathed in the sink."),
            ("Hij badde elke avond.", "He took a bath every evening."),
            ("We badden in het hotel.", "We bathed at the hotel."),
            ("Zij badden in het meer.", "They bathed in the lake."),
        ],
    },
    {
        "verb": "48. danken (regelmatig)",
        "sentences": [
            ("Ik dankte haar voor de hulp.", "I thanked her for the help."),
            ("Jij dankte de spreker.", "You thanked the speaker."),
            ("Hij dankte iedereen persoonlijk.", "He thanked everyone personally."),
            ("We dankten voor het eten.", "We said thanks for the meal."),
            ("Zij dankten het publiek.", "They thanked the audience."),
        ],
    },
    {
        "verb": "49. feesten (regelmatig)",
        "sentences": [
            ("We feestten tot de ochtend.", "We partied until the morning."),
            ("Jij feestte te hard gisteren.", "You partied too hard yesterday."),
            ("Hij feestte met zijn vrienden.", "He partied with his friends."),
            ("Ik feestte niet vaak.", "I did not party often."),
            ("Zij feestten in de stad.", "They partied in the city."),
        ],
    },
    {
        "verb": "50. missen (regelmatig)",
        "sentences": [
            ("Ik miste de trein.", "I missed the train."),
            ("Jij miste de laatste bus.", "You missed the last bus."),
            ("Hij miste zijn familie.", "He missed his family."),
            ("We misten een belangrijke clue.", "We missed an important clue."),
            ("Zij misten nooit een wedstrijd.", "They never missed a match."),
        ],
    },
]


class DutchVerbsImperfectumPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(40, 80, 120)
        self.cell(
            0,
            10,
            "Dutch Verbs - Imperfect (Onvoltooid Verleden Tijd)",
            0,
            1,
            "C",
        )
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def add_verb_table(self, verb_data):
        verb_name = verb_data["verb"]
        sentences = verb_data["sentences"]

        table_height = 8 + (len(sentences) * 8) + 10
        if self.get_y() + table_height > 270:
            self.add_page()

        self.set_font("Helvetica", "B", 11)
        self.set_text_color(50, 50, 50)
        self.set_fill_color(220, 235, 250)
        self.cell(0, 8, verb_name, 0, 1, "L", fill=True)

        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(70, 130, 180)
        self.set_text_color(255, 255, 255)
        self.cell(95, 7, "Dutch Sentence", 1, 0, "C", fill=True)
        self.cell(95, 7, "English Translation", 1, 1, "C", fill=True)

        self.set_font("Helvetica", "", 9)
        self.set_text_color(40, 40, 40)

        for i, (dutch, english) in enumerate(sentences):
            if i % 2 == 0:
                self.set_fill_color(245, 250, 255)
            else:
                self.set_fill_color(255, 255, 255)

            self.cell(95, 7, dutch, 1, 0, "L", fill=True)
            self.cell(95, 7, english, 1, 1, "L", fill=True)

        self.ln(5)


def create_pdf():
    pdf = DutchVerbsImperfectumPDF()
    pdf.add_page()

    for verb_data in verbs_data:
        pdf.add_verb_table(verb_data)

    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "dutch_verbs_imperfectum.pdf",
    )
    pdf.output(output_path)
    print(f"PDF created successfully: {output_path}")
    return output_path


if __name__ == "__main__":
    create_pdf()
