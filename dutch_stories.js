// Dutch Short Stories for Beginners
// Source: "Dutch Short Stories for Beginners" by Colleen Geske, Stuff Dutch People Like
// Add new stories by appending objects to this array.
const DUTCH_STORIES = [
  {
    title: "Een leuk gesprek in Haarlem",
    desc: "Twee mensen ontmoeten elkaar in een café in Haarlem en bespreken de verschillen tussen Nederland en de VS",
    paras: [
      `Esther loopt door de straten van Haarlem. Ze heeft zin in koffie en besluit om naar haar favoriete koffietentje te gaan. Ze bestelt een cappuccino en gaat zitten bij het raam. Na een paar minuten komt er een man naast haar zitten. Hij glimlacht vriendelijk en introduceert zichzelf als Mark.`,
      `"Hi, ik ben Mark. Ben je Nederlands?" vraagt hij met een Amerikaans accent.`,
      `"Ja, ik ben Nederlands. En jij?" antwoordt Esther.`,
      `"Ik kom uit Amerika, ik ben hier op vakantie. Het is zo'n mooi land. Hoe gaat het met je?" vraagt Mark.`,
      `"Goed, dank je. Ik geniet ook van ons land. Wat denk je tot nu toe van Nederland?" vraagt Esther.`,
      `"Ik vind het heel leuk, maar er zijn wel wat verschillen tussen Nederland en Amerika. Zo vind ik het interessant hoe direct Nederlanders zijn. In Amerika zijn we een beetje meer politiek correct," zegt Mark.`,
      `"Ja, dat klopt. We zijn heel direct. We zeggen vaak wat we denken. Is dat anders in Amerika?" vraagt Esther.`,
      `"Ja, dat is anders. In Amerika hebben we meer politieke correctheid. We proberen geen mensen te kwetsen met onze woorden. Maar soms kan het een beetje vermoeiend zijn om altijd politiek correct te moeten zijn," legt Mark uit.`,
      `"Ja, dat begrijp ik wel. Maar soms kan het ook wel een beetje hard overkomen als je te direct bent," antwoordt Esther.`,
      `"Ja, dat kan ook zo zijn. Maar het is ook wel verfrissend om te weten waar je aan toe bent," zegt Mark.`,
      `Esther en Mark praten verder over de verschillen tussen Nederland en Amerika. Ze hebben ook een interessant gesprek over eten.`,
      `"Ik hou van Nederlands eten. Ik heb al veel heerlijke dingen gegeten hier. Maar ik moet zeggen, ik mis wel het Amerikaanse fastfood," zegt Mark lachend.`,
      `"Ja, we hebben hier niet zoveel fastfood. Maar ik denk dat dat ook wel goed is. Het is niet zo gezond," antwoordt Esther.`,
      `"Ja, dat is waar. Maar soms heb ik gewoon zin in een goede hamburger of frietjes," zegt Mark.`,
      `"Je moet echt onze bitterballen proberen. Dat is een typisch Nederlands snack. Ze zijn zo lekker," zegt Esther.`,
      `"Oké, ik zal het proberen. En jij moet de Amerikaanse pizza eens proberen. Het is echt anders dan de Italiaanse pizza," zegt Mark.`,
      `Esther en Mark praten nog een tijdje verder over eten en cultuur. Na een tijdje nemen ze afscheid en gaan ze ieder hun eigen weg.`,
      `Esther voelt zich blij dat ze een nieuwe vriend heeft ontmoet uit een ander land. Het was een interessant gesprek en ze heeft veel geleerd over de Amerikaanse cultuur. Ze neemt zich voor om in de toekomst nog meer te praten met mensen uit andere culturen.`
    ],
    vocab: [
      ["koffietentje", "coffee shop"],
      ["tot nu toe", "until now"],
      ["verschillen", "differences"],
      ["kwetsen", "to hurt"],
      ["vermoeiend", "tiring"],
      ["verfrissend", "refreshing"]
    ],
    questions: [
      "Wat betekent het volgens Esther dat Nederlanders direct zijn?",
      "Wat vindt Mark positief aan het direct zijn van Nederlanders?",
      "Waarom vindt Esther het goed dat er niet zoveel fastfood in Nederland is?"
    ]
  },
  {
    title: "Een dagje Amsterdam",
    desc: "Joost en Fieke besluiten een dagje naar Amsterdam te gaan en ontdekken de mooiste plekken van de stad",
    paras: [
      `Joost en Fieke zijn een stel dat graag samen dagjes uitgaat. Vandaag hebben ze besloten om naar Amsterdam te gaan. Ze hebben er veel zin in!`,
      `'s Morgens vroeg staan ze op en ontbijten ze samen. Daarna pakken ze hun spullen en vertrekken ze naar het station. Ze nemen de trein naar Amsterdam en genieten van het uitzicht onderweg.`,
      `Als ze in Amsterdam aankomen, voelen ze meteen de energie van de stad. Ze gaan eerst naar het Rijksmuseum. Joost houdt van schilderijen en Fieke houdt van geschiedenis, dus het museum is perfect voor hen beiden. Ze kijken hun ogen uit bij de kunstwerken en leren veel over de Nederlandse geschiedenis.`,
      `Na het museum hebben ze honger gekregen. Ze besluiten om naar een typisch Nederlands café te gaan en bestellen een broodje haring en een glas melk. Het is even wennen voor Fieke, maar Joost geniet van de vis. Na de lunch maken ze een wandeling langs de grachten en bekijken ze de mooie huizen en boten.`,
      `Dan besluiten ze om een rondvaart door de grachten te maken. Ze stappen op de boot en de kapitein vertelt over de geschiedenis van Amsterdam. Joost en Fieke vinden het erg interessant en maken veel foto's van de mooie gebouwen en bruggen.`,
      `Als de rondvaart is afgelopen, besluiten ze om naar het Anne Frank Huis te gaan. Het is een emotionele ervaring om te zien hoe Anne Frank en haar familie hebben geleefd tijdens de Tweede Wereldoorlog. Joost en Fieke zijn blij dat ze deze plek hebben bezocht en zijn dankbaar voor hun vrijheid.`,
      `Het is inmiddels laat in de middag en Joost en Fieke zijn moe van alle indrukken. Ze besluiten om terug te gaan naar het station en de trein naar huis te nemen. Ze kijken terug op een geweldige dag en zijn blij dat ze dit samen hebben kunnen doen.`
    ],
    vocab: [
      ["ik heb zin in", "I feel like doing it"],
      ["'s morgens", "in the morning"],
      ["van iets houden", "to like / love something"],
      ["schilderij", "painting"],
      ["geschiedenis", "history"],
      ["wennen", "to get used to something"],
      ["inmiddels", "meanwhile"],
      ["geweldig", "awesome"]
    ],
    questions: [
      "Waarom is het Rijksmuseum een goed museum om te bezoeken voor het stel?",
      "Wat vindt Fieke van de Nederlandse lunch?",
      "Waarom zijn Joost en Fieke dankbaar na het bezoeken van het Anne Frank Huis?"
    ]
  },
  {
    title: "Een romantische ontmoeting in Rotterdam",
    desc: "Anna ontmoet Tim in een café en ze worden verliefd, maar het leven gooit roet in het eten",
    paras: [
      `Anna woont al haar hele leven in Rotterdam. Ze houdt van de stad en alles wat er te doen is. Op een dag ontmoet ze een jonge man die Tim heet. Tim is nieuw in de stad en is hier om te studeren. Anna en Tim ontmoeten elkaar toevallig in een café en beginnen te praten. Ze voelen zich meteen tot elkaar aangetrokken.`,
      `In de weken die volgen, zien Anna en Tim elkaar vaak. Ze gaan naar de markt, bezoeken museums en maken wandelingen langs de rivier. Ze genieten van elkaars gezelschap en leren elkaar steeds beter kennen. Anna merkt dat ze sterke gevoelens heeft voor Tim. Ze is verliefd op hem.`,
      `Op een avond neemt Tim Anna mee naar een speciale plek in de stad. Het is een klein parkje midden in het centrum van Rotterdam. Het parkje is rustig en er zijn bijna geen mensen. Tim neemt Anna mee naar een bankje en begint te praten. Hij vertelt haar dat hij verliefd op haar is en dat hij hoopt dat zij ook gevoelens voor hem heeft.`,
      `Anna is verrast, maar ook blij. Ze vertelt Tim dat ze ook verliefd op hem is en dat ze graag een relatie met hem wil hebben. Tim is blij en ze beginnen te zoenen. Het is een romantisch moment en Anna voelt zich gelukkiger dan ooit tevoren.`,
      `In de weken die volgen, is Anna nog meer verliefd op Tim. Ze gaan samen uit eten, maken lange wandelingen en gaan zelfs op een romantisch weekendje weg naar een andere stad. Anna kan haar geluk niet op. Ze is zo blij dat ze Tim heeft ontmoet en dat ze nu een relatie hebben.`,
      `Maar op een dag gebeurt er iets vreselijks. Tim krijgt een ongeluk en moet naar het ziekenhuis. Anna is wanhopig en bang dat hij niet zal herstellen. Ze zit dagen en nachten naast zijn bed en hoopt dat hij snel beter zal worden. Maar het duurt lang en Anna is moe en verdrietig.`,
      `Uiteindelijk herstelt Tim en kan hij het ziekenhuis verlaten. Anna is blij en opgelucht. Ze beseft dat ze nog meer van hem houdt dan ze ooit heeft gedaan. Ze besluit om hem te vragen om samen te wonen. Tim is blij en stemt toe. Ze beginnen samen een nieuw leven in Rotterdam en zijn gelukkiger dan ooit tevoren.`
    ],
    vocab: [
      ["ontmoeten", "to meet"],
      ["toevallig", "accidentally / by chance"],
      ["wandeling", "stroll"],
      ["gezelschap", "company (of people)"],
      ["gevoelens", "feelings"],
      ["verliefd", "in love"],
      ["vreselijk", "horrible"],
      ["zoenen", "kissing"],
      ["wanhopig", "in despair"],
      ["verdrietig", "sad"],
      ["opgelucht", "relieved"]
    ],
    questions: [
      "Hoe hebben Tim en Anna elkaar ontmoet? (Waar, was het gepland, …?)",
      "Waar vertelt Tim aan Anna dat hij verliefd op haar is?",
      "Waarom vraagt Anna of Tim met haar samen wil wonen?"
    ]
  },
  {
    title: "Een diefstal in Groningen",
    desc: "Detective Mark lost een schilderijdiefstal op uit het Groninger Museum",
    paras: [
      `In de stad Groningen is het rustig. Maar dan gaat de telefoon van de lokale detective, Mark. Er is een schilderij gestolen uit het Groninger Museum, en het museumpersoneel heeft geen idee wie het heeft meegenomen.`,
      `Mark gaat meteen naar het museum om de situatie te onderzoeken. Hij bekijkt de beveiligingscamera's en ziet een man met een hoed het museum binnenkomen en weer vertrekken met het schilderij onder zijn arm.`,
      `Mark vraagt het personeel of ze de man kennen, maar niemand herkent hem.`,
      `Mark besluit om verder te onderzoeken. Hij kijkt naar het gezicht van de man en naar wat er opvalt aan zijn hoed en zijn jas. Hij besluit om naar de hoedenwinkel en de kledingzaak in de buurt te gaan en vraagt of ze hem kunnen helpen.`,
      `De eigenaar van de hoedenwinkel herkent de man en vertelt Mark dat hij de hoed een paar dagen geleden heeft verkocht. Mark vraagt om de naam van de man, maar de eigenaar kan hem niet helpen. De eigenaar zegt wel dat de man op een verlaten boerderij woont, dus Mark besluit daar eens naar te kijken.`,
      `Wanneer Mark bij de boerderij aankomt, ziet hij een auto staan. Na een tijdje komt er een man uit de boerderij die inderdaad de hoed draagt die hij op de beveiligingscamera zag. Mark vraagt om zijn naam en de man zegt dat hij Jan heet.`,
      `Mark vraagt Jan waarom hij het schilderij heeft gestolen, en Jan vertelt hem dat hij het schilderij nodig heeft om zijn zieke moeder te helpen. Mark vindt dit heel zielig. Hij gaat terug naar het museum en praat met de directeur. De directeur besluit om Jan het schilderij te laten houden, zodat hij het kan verkopen om zijn moeder te helpen.`,
      `Jan is dankbaar en geeft het schilderij aan zijn moeder. Ze verkopen het voor een goed bedrag en gebruiken het geld om haar medische behandelingen te betalen. Mark is blij dat de zaak is opgelost en hij heeft kunnen helpen. Hij besluit om een goede fles wijn te kopen om te vieren.`
    ],
    vocab: [
      ["diefstal", "theft"],
      ["schilderij", "painting"],
      ["beveiliging", "security"],
      ["onderzoek", "investigation"],
      ["boerderij", "farm"],
      ["inderdaad", "indeed"],
      ["zielig", "sad / pitiful"],
      ["besluiten", "to decide"],
      ["behandeling", "treatment"],
      ["opgelost", "solved"],
      ["dankbaar", "thankful"],
      ["vieren", "to celebrate"]
    ],
    questions: [
      "Welk kledingstuk helpt Mark bij het oplossen van de diefstal?",
      "Waarom heeft Jan het schilderij gestolen?",
      "Wat doet Mark om te vieren dat hij de diefstal heeft opgelost?"
    ]
  },
  {
    title: "Teun wordt bakker",
    desc: "Teun geeft zijn saaie kantoorbaan op en volgt zijn droom om bakker te worden in Gouda",
    paras: [
      `Teun zit achter zijn bureau op kantoor. Hij staart naar het computerscherm en zucht diep. Hij haat zijn baan. Het is saai en hij voelt zich opgesloten tussen vier muren. Hij denkt na over wat hij echt graag zou willen doen. Plotseling herinnert hij zich dat hij als kind graag taarten bakte met zijn moeder. Hij vraagt zich af waarom hij niet gewoon een bakkerij begint.`,
      `Diezelfde dag nog gaat hij naar de bibliotheek en leent hij een stapel boeken over bakken. Hij leest alles wat hij kan vinden over brood, taarten en gebak. Hij bakt thuis een paar keer en geeft het resultaat aan vrienden en familie. Ze zijn verrast over hoe lekker het smaakt.`,
      `Teun besluit dat het tijd is om zijn droom te realiseren. Hij zoekt een locatie en vindt een klein winkelpand in Gouda. Hij koopt ovens, mixers en andere apparatuur. Hij begint vroeg in de ochtend met bakken en opent zijn winkel om acht uur.`,
      `In het begin gaat het moeizaam. Hij heeft niet veel klanten en het kost tijd om bekend te worden. Maar langzaam maar zeker begint zijn bakkerij populairder te worden. Overal vandaan komen mensen om zijn versgebakken brood te kopen. Zijn taarten zijn de lekkerste van de stad.`,
      `Op een dag komt er een journalist langs die een artikel wil schrijven over zijn bakkerij. Het artikel wordt gepubliceerd in de krant en daarna gaat het hard. De bakkerij wordt steeds bekender en hij krijgt steeds meer klanten.`,
      `Teun kan zijn geluk niet op. Hij doet iets wat hij echt leuk vindt en hij verdient er ook nog eens zijn geld mee. Hij voelt zich vrijer dan ooit tevoren en is trots op wat hij heeft bereikt.`
    ],
    vocab: [
      ["kantoor", "office"],
      ["zuchten", "to sigh"],
      ["saai", "boring"],
      ["muren", "walls"],
      ["plotseling", "suddenly"],
      ["zich herinneren", "to remember"],
      ["lenen", "to borrow"],
      ["verrast zijn", "to be surprised"],
      ["moeizaam", "difficult / arduous"],
      ["klant", "customer"],
      ["krant", "newspaper"],
      ["bekend", "known / famous"],
      ["verdienen", "to earn"],
      ["trots", "proud"]
    ],
    questions: [
      "Wanneer is Teuns liefde voor bakken begonnen?",
      "Is de bakkerij van Teun meteen een succes? Waarom wel / niet?",
      "Welke gebeurtenis zorgt ervoor dat de bakkerij heel populair wordt?"
    ]
  },
  {
    title: "De tweeling",
    desc: "Sietske ontdekt op het strand een meisje dat precies op haar lijkt — haar tweelingzus Petra",
    paras: [
      `Er is een meisje dat Sietske heet. Ze woont met haar ouders in een klein dorpje aan de rand van de stad. Sietske is een gelukkig meisje, maar soms vraagt ze zich af of er nog iemand anders is zoals zij.`,
      `Op een dag, tijdens de vakantie, besluiten Sietske's ouders om een reis naar het strand te maken. Terwijl Sietske op het strand loopt, ziet ze een meisje dat er precies uitziet als zij. Het meisje heet Petra en ze blijkt Sietske's tweelingzus te zijn!`,
      `Petra en Sietske raken al snel bevriend. Ze ontdekken dat ze veel gemeen hebben, maar ook dat ze op sommige vlakken heel anders zijn. Zo houdt Sietske van tekenen en schilderen, terwijl Petra meer van sporten houdt.`,
      `De meisjes besluiten om hun vakantie samen door te brengen en genieten van elkaars gezelschap. Ze maken lange wandelingen langs de zee, bouwen zandkastelen en verzamelen schelpen. Ze praten over van alles en nog wat en ontdekken steeds meer over elkaar.`,
      `Op een dag besluiten ze om te kijken waarom ze zo op elkaar lijken. Ze vragen het aan hun ouders en komen erachter dat ze beide geadopteerd zijn. Dit verklaart waarom ze bij verschillende families opgroeien. Sietske en Petra zijn verbaasd en een beetje geschrokken, maar ze realiseren zich al snel dat ze nog steeds familie zijn en dat ze elkaar altijd kunnen bellen als ze elkaar missen.`,
      `De vakantie loopt ten einde en de meisjes moeten afscheid van elkaar nemen. Ze beloven om elkaar elke dag te bellen en te schrijven. Als Sietske en haar ouders weer thuis zijn, belt ze meteen naar Petra. Het is alsof ze elkaar al jaren kennen en ze hebben veel te bespreken.`,
      `Sietske is erg blij dat ze haar tweelingzus heeft gevonden. Ze realiseert zich dat ze niet alleen is en dat er iemand is die net zo is als zij. Ze weet dat ze altijd op Petra kan rekenen en dat ze elkaar nooit zullen vergeten. Ze kijkt uit naar de dag dat ze elkaar weer kunnen zien. Sietske en Petra zijn misschien niet op dezelfde plek opgegroeid, maar ze hebben nu wel een sterke band voor het leven.`
    ],
    vocab: [
      ["terwijl", "while"],
      ["uitzien", "to look (like)"],
      ["ontdekken", "to discover"],
      ["tweeling", "twin"],
      ["gezelschap", "company (people)"],
      ["besluiten", "to decide"],
      ["afscheid", "farewell"],
      ["op iemand rekenen", "to count on someone"],
      ["opgegroeid", "grown up"]
    ],
    questions: [
      "Wat zijn verschillen tussen Petra en Sietske?",
      "Hoe komt het dat Petra en Sietske niet samen zijn opgegroeid?",
      "Op welke manier houden Petra en Sietske contact na de vakantie?"
    ]
  },
  {
    title: "Fred komt op bezoek",
    desc: "Tom vindt een verdwaald buitenaards wezen van Mars en sluit een onverwachte vriendschap",
    paras: [
      `Op een dag crasht er een ruimteschip op aarde en er komt een klein groen mannetje uit. Het mannetje heet Fred en komt van de planeet Mars. Hij heeft honger en is koud en verdwaald. Hij heeft ook geen idee hoe hij weer thuis moet komen.`,
      `Op dat moment komt Tom, een jongen van 10 jaar, terug van school. Hij ziet het ruimteschip en rent ernaartoe om te kijken wat er aan de hand is. Als hij dichterbij komt, ziet hij het kleine groene mannetje dat op de grond zit en huilt.`,
      `Tom is verbaasd en vraagt zich af of het een buitenaards wezen is. Maar hij voelt medelijden en besluit hem te helpen.`,
      `Tom neemt het mannetje mee naar huis en geeft hem te eten en drinken. Hij geeft hem ook een warme deken om onder te liggen. Fred voelt zich beter en begint te glimlachen. Hij gebaart dat hij Tom wil bedanken. Tom kan de gebaren van Fred niet begrijpen, maar hij begrijpt wel dat hij blij is.`,
      `Tom besluit om Fred in zijn kamer te verstoppen zodat niemand hem kan vinden. Hij vertelt zijn ouders niet over de kleine groene man, omdat hij bang is dat ze hem naar de autoriteiten zullen brengen. In plaats daarvan besluit Tom om voor Fred te zorgen.`,
      `Dagen gaan voorbij en Tom en Fred worden goede vrienden. Ze spelen samen en hebben veel plezier. Tom leert zelfs wat woorden in het Martian, de taal van Fred. Fred is heel blij dat hij een vriend heeft en voelt zich niet meer alleen.`,
      `Maar op een nacht gebeurt er iets onverwachts. Een groot ruimteschip landt in de tuin van Tom. Fred springt op en gebaart dat het zijn familie is. Tom is verdrietig omdat hij weet dat Fred weggaat, maar hij is ook blij voor hem omdat hij weet dat Fred weer thuis zal zijn.`,
      `Freds familie neemt hem mee in het ruimteschip en voordat ze weggaan, zwaaien ze naar Tom. Tom zwaait terug en voelt zich blij voor Fred, maar ook een beetje verdrietig omdat zijn vriend weggaat.`,
      `Maar dan beseft Tom dat hij niet alleen is. Hij heeft zijn familie en vrienden op aarde en hij weet dat hij Fred via het intergalactische internet kan blijven spreken. Hij is blij dat hij een vriend heeft gevonden, zelfs als die vriend van een andere planeet komt.`,
      `Tom gaat naar bed en valt in slaap met een glimlach.`
    ],
    vocab: [
      ["ruimteschip", "spaceship"],
      ["verdwaald", "lost"],
      ["wat er aan de hand is", "what's going on"],
      ["dichterbij", "closer"],
      ["huilen", "to cry"],
      ["gebaren", "to gesture"],
      ["verbaasd", "surprised"],
      ["medelijden", "pity"],
      ["deken", "blanket"],
      ["glimlach", "smile"],
      ["verstoppen", "to hide"],
      ["bang", "afraid"],
      ["in plaats van", "instead of"],
      ["onverwachts", "unexpected"],
      ["zwaaien", "to wave"]
    ],
    questions: [
      "Wat is Toms eerste reactie als hij het ruimteschip ziet?",
      "Waarom vertelt Tom niemand over Fred?",
      "Wat vindt Tom ervan als Fred weer terug naar zijn familie gaat?"
    ]
  },
  {
    title: "Femke en de diamantendief",
    desc: "Detective Femke lost een diamantdiefstal op in Amsterdam en vindt daarbij ook liefde",
    paras: [
      `Femke is een detective in Amsterdam. Ze houdt van haar werk. Vandaag begint ze aan een nieuwe zaak. Een juwelier in het centrum van de stad heeft haar gebeld omdat er een diamant gestolen is uit zijn winkel.`,
      `Femke begint met het verzamelen van bewijsmateriaal. Ze praat met getuigen en kijkt naar de beelden van de beveiligingscamera's. Na een paar uur werken heeft ze genoeg informatie om de zaak op te lossen.`,
      `Ze besluit om naar het Rijksmuseum te gaan. Ze heeft gehoord dat de dief misschien de diamant probeert te verkopen aan een van de kunsthandelaren daar. Als ze het museum binnenkomt, ziet ze een verdacht uitziende man rondlopen. Ze besluit hem te volgen en ziet hem naar een kunsthandelaar gaan.`,
      `Femke gaat naar de kunsthandelaar en vraagt of hij misschien iets weet over de gestolen diamant. De kunsthandelaar ontkent iets te weten, maar Femke is niet overtuigd. Ze vraagt hem om zijn beveiligingsbeelden te bekijken en ziet de dief die de diamant aan hem probeert te verkopen.`,
      `Femke gaat terug naar de verdachte man en arresteert hem. Hij bekent de diamant gestolen te hebben en geeft hem terug aan de juwelier. Femke heeft de zaak opgelost en de diamant is teruggebracht naar de rechtmatige eigenaar.`,
      `De juwelier is zo blij dat hij Femke uitnodigt voor een feestje om haar te bedanken. Femke gaat naar het feestje en ontmoet daar een charmante man. Ze praten met elkaar en hebben veel gemeen. Aan het eind van de avond vraagt hij haar uit voor een etentje de volgende avond. Femke stemt toe en ze hebben een geweldige avond samen.`,
      `Femke realiseert zich dat de zaak haar niet alleen een opgeloste misdaad heeft opgeleverd, maar ook een nieuw contact en misschien wel iets meer.`
    ],
    vocab: [
      ["verzamelen", "to collect"],
      ["bewijsmateriaal", "evidence"],
      ["kunsthandelaar", "art dealer"],
      ["verdacht uitziende", "suspicious looking"],
      ["misschien", "maybe"],
      ["ontkennen", "to deny"],
      ["overtuigd", "convinced"],
      ["bekent", "admits"],
      ["opgelost", "solved / resolved"]
    ],
    questions: [
      "Wat wil de diamantendief met de gestolen diamant doen?",
      "Heeft de diamantendief de diamant al aan een kunsthandelaar verkocht? Waarom denk je van wel / niet?",
      "Wat doet de juwelier om Femke te bedanken?"
    ]
  },
  {
    title: "Pieter heeft een droom",
    desc: "In de Gouden Eeuw van Amsterdam vecht Pieter voor zijn liefde voor Lotte ondanks sociale obstakels",
    paras: [
      `In 17e-eeuws Amsterdam leeft een man genaamd Pieter. Hij is verliefd op Lotte. Hoewel ze ook van hem houdt, kan ze niet met hem samen zijn omdat ze van koninklijke bloedlijn is en haar familie hier niet mee akkoord gaat.`,
      `Pieter werkt hard en wordt een succesvolle handelaar in Amsterdams Gouden Eeuw. Ondertussen verliest Lotte's familie veel geld en worden ze arm. Maar Pieter blijft hard werken aan zijn droom.`,
      `Op een dag, wanneer Pieter en Lotte elkaar weer ontmoeten, ziet Lotte hoe succesvol Pieter is geworden. Haar familie is nog steeds tegen hun relatie. Pieter geeft niet op en blijft hard werken, totdat hij zoveel geld heeft verdiend dat zelfs de koninklijke familie onder de indruk is.`,
      `Lotte's familie accepteert nu de relatie tussen Pieter en Lotte en ze trouwen in een prachtige ceremonie. Samen genieten ze van hun succes en leven ze nog lang en gelukkig.`,
      `Het is een verhaal over vastberadenheid en liefde die overwint. Het laat zien dat met hard werken en doorzettingsvermogen alles mogelijk is. En wie weet, misschien kunnen we allemaal ons eigen geluk vinden in de wereld, net zoals Pieter dat heeft gedaan.`
    ],
    vocab: [
      ["17e eeuw", "17th century"],
      ["hoewel", "although"],
      ["gouden eeuw", "golden age"],
      ["ondertussen", "meanwhile"],
      ["verliezen", "to lose"],
      ["arm", "poor"],
      ["opgeven", "to give up"],
      ["onder de indruk", "impressed"],
      ["vastberadenheid", "determination"],
      ["doorzettingsvermogen", "perseverance"]
    ],
    questions: [
      "Waarom vindt de familie van Lotte het in het begin niet goed dat Lotte en Pieter samen willen zijn?",
      "Om welke twee redenen vindt de familie van Lotte het uiteindelijk wel goed dat Lotte en Pieter samen zijn?",
      "Wat kunnen we volgens de schrijver leren van dit verhaal?"
    ]
  },
  {
    title: "Klaas en de pieten",
    desc: "Klaas ontdekt dat hij de laatste afstammeling van Sinterklaas is en moet de rol op zich nemen",
    paras: [
      `Klaas is een gewone man die in Nederland woont. Hij werkt hard en leeft een rustig leven. Hij heeft altijd genoten van de Sinterklaasviering, waarbij kinderen cadeautjes krijgen van "Sint" en zijn helpers, de Pieten.`,
      `Maar de laatste 10 jaar heeft niemand Sinterklaas meer gezien. Sommige mensen denken dat hij gestopt is met het brengen van cadeautjes, anderen denken dat hij niet meer bestaat. Maar op een dag verandert alles voor Klaas.`,
      `Op een ochtend krijgt Klaas een brief in zijn brievenbus. Hij opent de brief en leest dat hij de laatste afstammeling is van Sinterklaas. Hij moet nu de rol van de goedheiligman overnemen en cadeautjes brengen naar alle kinderen in Nederland op 5 december.`,
      `Klaas is verbaasd en weet niet wat hij moet doen. Hij heeft geen ervaring in het brengen van cadeautjes en ook geen ervaring met paarden. Maar hij besluit de uitdaging aan te gaan en begint zich voor te bereiden.`,
      `Hij oefent elke dag met het paard van zijn buurman en leert hoe hij cadeautjes moet inpakken. Hij ontdekt ook dat de Pieten hem zullen helpen. Ze zijn kleurrijk gekleed en zien er erg vriendelijk uit. Klaas begint zich steeds zekerder te voelen en kijkt uit naar 5 december.`,
      `Op de avond van 5 december begint Klaas aan zijn taak. Hij rijdt op zijn witte paard dat "Oh zo snel" heet, en heeft een grote zak vol cadeautjes bij zich. De Pieten zijn bij hem en helpen hem om de cadeautjes te bezorgen.`,
      `Maar al snel wordt het duidelijk dat het niet makkelijk is om alle cadeautjes te bezorgen. Sommige huizen zijn moeilijk te vinden en sommige kinderen slapen al. Klaas en de Pieten blijven hard werken en geven niet op.`,
      `Op een gegeven moment komen ze bij een huis waar geen schoorsteen is. Klaas en de Pieten weten niet hoe ze binnen moeten komen. Ze besluiten om door het raam te gaan. Maar dan gaat het mis. Klaas blijft vastzitten in het raam en kan niet meer bewegen.`,
      `De Pieten proberen hem te bevrijden, maar het lukt niet. Klaas begint te zweten en raakt in paniek. Maar dan hoort hij het geluid van kinderen die zingen en lachen. Hij beseft dat hij niet op moet geven en dat hij de cadeautjes moet bezorgen.`,
      `Met veel moeite weet hij zich los te maken en gaat hij weer verder met het bezorgen van de cadeautjes. Uiteindelijk lukt het hem om alle cadeautjes te bezorgen en keert hij terug naar huis.`,
      `Klaas is moe, maar ook trots. Hij heeft laten zien dat hij net zo'n goede Sinterklaas is als zijn voorouders. Hij zal de rol van Sint blijven vervullen en elk jaar cadeautjes brengen naar alle kinderen in Nederland. En hij weet dat hij altijd hulp zal hebben van zijn vriendelijke Pieten.`
    ],
    vocab: [
      ["gewoon", "normal"],
      ["sinterklaas", "a Dutch version of Santa Claus"],
      ["cadeautjes", "presents"],
      ["verandert", "changes"],
      ["afstammeling", "descendant"],
      ["goedheiligman", "saint"],
      ["uitdaging", "challenge"],
      ["buurman", "neighbor"],
      ["kleurrijk", "colourful"],
      ["moeite", "effort"],
      ["uiteindelijk", "finally"],
      ["voorouders", "ancestors"]
    ],
    questions: [
      "Wat doet Klaas om zich voor te bereiden op 5 december?",
      "Hoe bezorgt Klaas cadeaus bij een huis dat geen schoorsteen heeft?",
      "Waarom geeft Klaas niet op als zijn werk moeilijk is?"
    ]
  }
];
