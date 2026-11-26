# KTH category tree for Indico (proposal)

The category tree for a KTH-wide Indico, as a list to iterate on. Edit this file;
[`tree.py`](tree.py) checks it and exports it to the slide in the Swedish deck, and
[`make-categories.py`](make-categories.py) creates it in Indico. See the [README](README.md).

**Status: proposal.** Nothing here is agreed yet. Points to decide are listed under
[Open questions](#open-questions), and lines marked `<!-- check: … -->` need a look.

## Sources (read 2026-11-26)

- Top level: [KTH's organisation](https://intra.kth.se/en/styrning/kths-organisation/kth-s-organisation-1.3491),
  [University Administration](https://intra.kth.se/en/styrning/kths-organisation/verksamhetsstod).
- Faculty Council and its committees: the
  [Faculty Council pages](https://intra.kth.se/styrning/kths-organisation/kths-fakultetsrad/fakultetsradet-1.972900)
  (the Faculty Renewal Committee is only on the Swedish page).
- Faculty boards and their committees: each school's faculty board page (English names from the
  English version's menu), linked from
  [KTH Schools](https://intra.kth.se/en/styrning/kths-organisation/kth-s-skolor-1.3848).
- Line organisation and codes (school → department → division, University Administration →
  department → unit): the public [staff directory](https://www.kth.se/directory), read with
  [`fetch-directory.py`](fetch-directory.py). Names as the directory gives them.
- PriU groups: [the PriU page](https://www.kth.se/social/group/prioriterade-fragor/page/priu-grupper/).
- Research centres: [list of competence centres](https://intra.kth.se/en/forskning/leda-forskning/forskningscentrum/lista-over-centrumbildningar-1.1192887),
  names as listed there.

## Format

One category per line, two spaces of indent per level:

```
- `SHR` Particle Physics, Astrophysics & Medical Imaging · *Partikelfysik, astrofysik och medicinsk bildfysik*
```

- `` `SHR` ``: KTH organisation code, only for units in the line organisation. This is the
  key for linking a category to UG/LDAP groups later. Codes must be unique.
- Then the title the category gets in Indico.
- ` · *…*`: the name in the other language, for reference. Not used by Indico.
- `<!-- … -->` at the end of a line: a note, shown as a marker on the slide.

## Open questions

1. **Language of titles.** English titles, Swedish in italics. Swedish-only groups (PriU groups,
   Storträffar) have Swedish titles. Or Swedish throughout?
2. **Schools at the top level**, or under a "Schools" category? At the top level the path is
   short: KTH » SCI » Physics » PAM.
3. **How deep?** Divisions (three letters) and University Administration units (four letters)
   are included. Many may never hold a meeting. Create them all up front, or on request?
4. **EECS has no department level** in the directory: it lists divisions directly under the
   school (JH…, JJ…, JM…, JR…). Add the departments by hand?
5. **Shared and service units** (workshops, "common" units, units named like their
   department) are marked `check`. Drop, merge or keep?
6. **First and second cycle education:** its own top-level category, or under the Faculty
   Council's First and Second Cycle Education Committee? Swedish names of the networks?
7. **Research centres:** a flat list, or each centre under its host school? Centres hosted by
   another university (marked UU, LU) are KTH nodes; keep them?
8. **School committees:** English names as on each faculty board's English pages (Recruitment,
   Docent and Election Committee). EECS's English pages list only the Election Committee. CBH and
   SCI also list management groups and councils (ledningsgrupp, prefektråd, programråd,
   doktorandråd); add them?
9. **Protection.** `make-categories.py` makes every top-level category *protected*, as
   decided for the pilot; everything below inherits. Appointment committees stay protected
   whatever is decided for the rest. The Sandbox is opened by hand.

## Tree

<!-- tree:begin -->
- Central Management · *Central ledning*
  - University Board · *Universitetsstyrelsen*
  - `TA` President and Management · *Rektor och ledning* <!-- directory: under University Administration -->
  - KTH Management Group · *KTH:s ledningsgrupp*
  - `TP` Internal Audit · *Internrevisionen* <!-- directory: under University Administration -->
- Faculty Council · *Fakultetsrådet*
  - Ethics Committee · *Etikutskottet*
  - Third Cycle Education Committee · *Forskarutbildningsutskottet*
  - First and Second Cycle Education Committee · *Grundutbildningsutskottet*
  - Faculty Renewal Committee · *Fakultetsförnyelseutskottet* <!-- English name translated; the page is Swedish only -->
  - Promotion Board · *Befordringsutskottet*
  - KTH's Collegial Forum · *KTH kollegialt forum*
  - KTH's Language Committee · *KTH:s språkkommitté*
- First and Second Cycle Education · *Utbildning på grundnivå och avancerad nivå*
  - PriU-grupper · *PriU groups*
    - Arbetsliv och samverkan
    - Bedömnings- och examinationsmetoder
    - Digitalisering
    - Education and sustainability
    - Framtidens lärandemiljöer, schema och planering
    - KTH-lärares kompetens och utveckling
    - JML – Jämställdhet, mångfald och lika villkor
    - Studentens perspektiv och inflytande
    - Vilande och avslutade PriU-grupper · *Dormant and closed PriU groups*
  - Network for Programme Directors <!-- Swedish name? -->
  - Network for Directors of Studies <!-- Swedish name? -->
  - Joint Network for Programme Directors and Directors of Studies <!-- Swedish name? -->
  - Storträffar <!-- always in Swedish -->
- `A` School of Architecture and the Built Environment (ABE) · *Skolan för arkitektur och samhällsbyggnad*
  - Faculty Board ABE · *Fakultetsnämnd ABE*
    - Recruitment Committee · *Anställningsutskott*
    - First and Second Cycle Education Committee · *Grundutbildningsutskott*
    - Third-cycle Education Committee · *Forskarutbildningsutskott*
    - Impact Committee · *Impactutskott*
    - Docent Committee · *Docentutskott*
    - Election Committee · *Valberedning för Fakultetsnämnd ABE*
  - `AF` Civil & Architectural Engineering · *Byggvetenskap*
    - `AFB` Building Materials · *Byggnadsmaterial*
    - `AFK` Building Technology & Design · *Byggteknik och design*
    - `AFN` Civil & Architectural Engineering Laboratory · *Byggvetenskaps laboratorium*
    - `AFF` Concrete Structures · *Betongbyggnad*
    - `AFV` Highway & Railway Engineering · *Väg- och banteknik*
    - `AFH` Soil & Rock Mechanics · *Jord- och bergmekanik*
    - `AFE` Structural Engineering & Bridges · *Brobyggnad inklusive stålbyggnad*
    - `AFT` Sustainable Buildings · *Hållbara byggnader*
    - `AFP` Transport Planning · *Transportplanering*
  - `AK` Philosophy & History of Technology · *Filosofi och historia*
    - `AKC` History of Science, Technology & Environment · *Historiska studier*
    - `AKB` Philosophy · *Filosofi*
  - `AI` Real Estate & Construction Management · *Fastigheter och byggande*
    - `AID` Construction & Facilities Management · *Ledning och organisering i byggande och förvaltn*
    - `AIE` Real Estate Business & Financial Systems · *Fastighetsföretagande och finansiella system*
    - `AIB` Real Estate Economics & Finance · *Fastighetsekonomi och finans*
    - `AIJ` Surveying–Geodesy, Land Law & Real Estate Planning · *Lantmäteri – Fastighetsvetenskap och geodesi*
  - `AD` School of Architecture · *Arkitekturskolan*
    - `ADF` Architectural Lighting Design · *Ljusdesign*
    - `ADI` Architecture & Culture · *Arkitektur, kultur och miljö*
    - `ADH` Architecture & Technology · *Arkitektur, teknik och teori*
    - `ADJ` Architecture & Urban Design · *Arkitektur, landskap och städer*
    - `ADG` Workshop & Labs · *Verkstad* <!-- check: shared or service unit, does it need its own category? -->
  - `AL` Sust. Development, Env. Science & Engineering · *Hållbar utveckling, miljövetenskap och teknik*
    - `ALK` Resources, Energy & Infrastructure · *Resurser, energi och infrastruktur*
    - `ALH` Strategic Sustainability Studies · *Strategiska hållbarhetsstudier*
    - `ALG` Sustainability Assessment & Management · *Hållbarhet, utvärdering och styrning*
    - `ALI` Water & Environmental Engineering · *Vatten- och miljöteknik*
  - `AG` Urban Planning & Environment · *Samhällsplanering och miljö*
    - `AGF` Geoinformatics · *Geoinformatik*
    - `AGI` Transport & Systems Analysis · *Transport och systemanalys*
    - `AGB` Urban & Regional Studies · *Urbana och regionala studier*
  - `ACP` Viable cities
- `J` School of Electrical Engineering and Computer Science (EECS) · *Skolan för elektroteknik och datavetenskap* <!-- the directory lists divisions directly under the school, no departments -->
  - Faculty Board EECS · *Fakultetsnämnd EECS*
    - Recruitment Committee · *Anställningsutskott EECS* <!-- English page lists only the Election Committee; names as for the other schools -->
    - Docent Committee · *Docentutskott EECS*
    - Election Committee · *Valberedning för Fakultetsnämnd EECS*
  - `JCP` Center for High Performance Computing · *Parallelldatorcentrum*
  - `JHF` Communication Systems · *Kommunikationssystem*
  - `JHS` Computational Science & Technology · *Beräkningsvetenskap och beräkningsteknik*
  - `JHK` Computing and Learning Systems · *Datatekniska och lärande system*
  - `JRL` Decision & Control Systems · *Reglerteknik*
  - `JJN` Electric Power & Energy Systems · *Elkraftteknik*
    - `JJNB` Sustainable Power Lab (SPL)
  - `JJF` Electromagnetics & Plasma Physics · *Elektromagnetism och plasmafysik*
  - `JJG` Electronics & Embedded Systems · *Elektronik och inbyggda system*
  - `JCB` Electrum Laboratory · *Electrumlaboratoriet*
  - `JRO` Information Science & Engineering · *Teknisk informationsvetenskap*
  - `JMA` Media Technology & Interaction Design · *Medieteknik och interaktionsdesign*
  - `JRQ` Micro & Nano Systems · *Mikro- och nanosystem*
  - `JHP` Network & Systems Engineering · *Nätverk och systemteknik*
  - `JRR` Robotics, Perception & Learning · *Robotik, perception och lärande*
  - `JRT` Speech, Music & Hearing · *Tal, musik och hörsel*
  - `JHT` Theoretical Computer Science · *Teoretisk datalogi*
- `M` School of Industrial Engineering and Management (ITM) · *Skolan för industriell teknik och management*
  - Faculty Board ITM · *Fakultetsnämnd ITM*
    - Recruitment Committee · *Anställningsutskott ITM*
    - Docent Committee · *Docentutskott ITM*
    - Election Committee · *Valberedning för Fakultetsnämnd ITM*
  - `MJE` Energy Technology · *Energiteknik*
    - `MJEB` Applied Thermodynamics & Refrigeration · *Tillämpad termodynamik och kylteknik*
    - `MJEM` Energy Systems · *Energisystem*
    - `MJEC` Heat & Power Technology · *Kraft- och värmeteknologi*
  - `MF` Engineering Design · *Maskinkonstruktion*
    - `MFN` Dynamical Complex Systems · *Dynamiska komplexa system*
    - `MFA` Engineering Design Common · *Gemensam verksamhet* <!-- check: shared or service unit, does it need its own category? -->
    - `MFG` Integrated Product Development & Design · *Integrerad produktutveckling*
    - `MFYB` Integrated Transport Research Lab
    - `MFC` Mechatronics · *Mekatronik*
    - `MFE` Systems & Component Design · *System- och komponentdesign*
  - `ME` Industrial Economics & Management · *Industriell ekonomi och organisation*
    - `MEZA` Management, Organisation & Governance · *Ledning, Organisering & Styrning*
    - `MEX` Sustainable Society · *Hållbart Samhälle*
    - `MEYA` Transition, Change and Industrial Dynamics · *Industriell Dynamik & Transformation*
  - `MO` Learning in Engineering Sciences · *Lärande*
    - `MOD` Digital Learning · *Digitalt lärande*
    - `MOG` House of Science · *Vetenskapens hus*
    - `MOE` Language & Communication · *Språk och kommunikation*
    - `MOB` Learning in STEM · *Lärande i STEM*
  - `MV` Materials Science & Engineering · *Materialvetenskap*
    - `MVC` Hultgren Laboratory
    - `MVD` Unit of Processes · *Enheten för processer*
    - `MVF` Unit of Properties · *Enheten för egenskaper*
    - `MVE` Unit of Structures · *Enheten för strukturer*
  - `MP` Production Engineering · *Produktionsutveckling*
    - `MPD` Manufacturing & metrology systems · *Tillverknings- och mätsystem*
    - `MPB` Production management & industrial systems · *Produktionsledning och industriella system*
    - `MPC` Production systems & automation · *Produktionssystem och automation*
- `C` School of Engineering Sciences in Chemistry, Biotechnology and Health (CBH) · *Skolan för kemi, bioteknologi och hälsa*
  - Faculty Board CBH · *Fakultetsnämnd CBH*
    - Recruitment Committee · *Anställningsutskott CBH*
    - Docent Committee · *Docentutskott CBH*
    - Election Committee · *Valberedning för Fakultetsnämnd CBH*
  - `CD` Biomedical Engineering & Health Systems · *Medicinteknik och hälsosystem*
    - `CDJ` Basic Science Education · *Grundläggande naturvetenskap*
    - `CDA` Biomedical Engineering & Health Systems · *Medicinteknik och hälsosystem* <!-- check: same name as its department, merge with it? -->
    - `CDG` Biomedical Imaging · *Medicinsk avbildning*
    - `CDI` Ergonomics · *Ergonomi*
    - `CDH` Health Informatics & Logistics · *Hälsoinformatik och logistik*
    - `CDE` Neuronic Engineering · *Neuronik*
  - `CF` Chemical Engineering · *Kemiteknik*
    - `CFG` Applied Electrochemistry · *Tillämpad elektrokemi*
    - `CFD` Energy Processes · *Energiprocesser*
    - `CFJ` Process Technology · *Processteknologi*
    - `CFF` Resource Recovery · *Resursåtervinning*
  - `CE` Chemistry · *Kemi*
    - `CEF` Applied Physical Chemistry · *Tillämpad fysikalisk kemi*
    - `CEG` Glycoscience · *Glykovetenskap*
    - `CED` Organic Chemistry · *Organisk kemi*
    - `CEE` Surface & Corrosion Science · *Yt- och korrosionsvetenskap*
    - `CEH` Theoretical Chemistry & Biology · *Teoretisk kemi och biologi*
  - `CM` Engineering Pedagogics · *Ingenjörspedagogik*
    - `CMA` Engineering Pedagogics · *Ingenjörspedagogik* <!-- check: same name as its department, merge with it? -->
  - `CG` Fibre & Polymer Technology · *Fiber- och polymerteknologi*
    - `CGI` Biocomposites · *Biokompositer*
    - `CGF` Coating Technology · *Ytbehandlingsteknik*
    - `CGA` Fibre & Polymer Technology · *Fiber- och polymerteknologi* <!-- check: same name as its department, merge with it? -->
    - `CGK` Fibre Processes · *Fiberprocesser*
    - `CGD` Polymer Technology · *Polymerteknologi*
    - `CGE` Polymeric Materials · *Polymera material*
    - `CGG` Wood Chemistry & Pulp Technology · *Träkemi och massateknologi*
  - `CHD` Gene Technology · *Genteknologi* <!-- check: directly under the school in the directory -->
  - `CBA` Greenhouse labs <!-- check: shared or service unit, does it need its own category? -->
  - `CK` Industrial Biotechnology · *Industriell bioteknologi*
    - `CKA` Industrial Biotechnology · *Industriell bioteknologi* <!-- check: same name as its department, merge with it? -->
  - `CJ` Protein Science · *Proteinvetenskap*
    - `CJE` Biomedical Proteomics · *Biomedicinsk proteomik*
    - `CJI` Drug Discovery & Development · *Läkemedelsutveckling*
    - `CJC` Nanobiotechnology · *Nanobioteknologi*
    - `CJH` Protein Engineering · *Proteinteknik*
    - `CJG` Protein Technology · *Proteinteknologi*
    - `CJD` Systems Biology · *Systembiologi*
- `S` School of Engineering Sciences (SCI) · *Skolan för teknikvetenskap*
  - Faculty Board SCI · *Fakultetsnämnd SCI*
    - Recruitment Committee · *Anställningsutskott SCI*
    - Docent Committee · *Docentutskott SCI*
    - Election Committee · *Valberedning för Fakultetsnämnd SCI*
  - `SK` Applied Physics · *Tillämpad fysik*
    - `SKA` Applied Physics Common · *Tillämpad fysik gemensam* <!-- check: shared or service unit, does it need its own category? -->
    - `SKB` Applied Physics Education · *Tillämpad fysik grundutbildning*
    - `SKS` Bio-Opto-Nano Physics · *Bio-opto-nano fysik*
    - `SKE` Biophysics · *Biofysik*
    - `SKT` Light & Matter Physics · *Ljus och materiens fysik*
    - `SKJ` Nanolab
  - `SM` Engineering Mechanics · *Teknisk mekanik*
    - `SME` Aerospace, Moveability & Naval Architecture · *Flyg och rymd/rörelsemekanik/MSY*
    - `SMF` Fluid Mechanics · *Strömningsmekanik*
    - `SMC` Material & Structural Mechanics · *Material- och strukturmekanik*
    - `SMD` Vehicle Engineering & Technical Acoustics · *Fordonsteknik och teknisk akustik*
  - `SF` Mathematics · *Matematik*
    - `SFH` Algebra, Combinatorics, Geometry & Topology · *Algebra kombinatorik & topolog*
    - `SFF` Analysis, Dynamics, Geometry, Number Theory & PDE · *Analys, dynamik, geometri, PDE och talteori*
    - `SFA` Mathematics Misc · *Institutionen för matematik* <!-- check: shared or service unit, does it need its own category? -->
    - `SFG` Numerical Analysis, Optimization & Systems Theory · *Numerik, optimering och system*
    - `SFI` Probability, Mathematical Physics & Statistics · *Probability, mathematical physics and statistics*
  - `SH` Physics · *Fysik*
    - `SHO` Condensed Matter Theory · *Kondenserade materiens teori*
    - `SHT` Nuclear Science & Engineering · *Kärnvetenskap och kärnteknik*
    - `SHR` Particle Physics, Astrophysics & Medical Imaging · *Partikelfysik, astrofysik och medicinsk bildfysik*
    - `SHS` Workshop · *Verkstad* <!-- check: shared or service unit, does it need its own category? -->
- `T` University Administration · *Verksamhetsstöd* <!-- President and Management (TA) and Internal Audit (TP) moved to Central Management -->
  - `TI` Communications Department · *Kommunikationsavdelningen*
    - `TIAJ` Channels & Systems Management · *Kanaler och system*
    - `TIAH` Education Communication & Brand · *Utbildningskommunikation och varumärke*
    - `TIAI` Management Communication & Press · *Ledningskommunikation och press*
    - `TIAG` Research Communication & News · *Forskningskommunikation och nyheter*
  - `TW` Cybercampus
    - `TWAA` Cybercampus Administration · *Administration Cybercampus*
  - `TG` Education Office · *Avdelningen för utbildningsstöd*
    - `TGC` Academic Registry · *Enheten för utbildningsadministration*
    - `TGB` International Relations Office · *Enhet Internationella relationer*
    - `TGA` Student's Office · *Enheten för studentservice*
  - `TD` Finance Department · *Ekonomiavdelningen*
    - `TDAA` Accounting Group · *Redovisningsgruppen*
    - `TDAD` Controller Group · *Controllergruppen*
    - `TDAF` Finance VS · *Ekonomi VS*
    - `TDAC` Ledger & System Support · *Betalningsflöden och systemsupport*
    - `TDAE` Procurement Group · *Upphandlingsgruppen*
  - `TE` Human Resources · *Personalavdelningen*
    - `TEBE` HR ABE, CBH & SCI · *HR ABE, CBH och SCI*
    - `TEBD` HR EECS & ITM · *HR EECS och ITM*
    - `TEBA` HR Support · *HR-Support*
    - `TEBF` HR University Administration · *HR VS*
    - `TEBC` Labour law & work environment · *Arbetsrätt och arbetsmiljö*
    - `TEAD` PA-speciellt <!-- check: shared or service unit, does it need its own category? -->
    - `TEBB` Professional Development & HR System · *Kompetensförsörjning och HR-system*
  - `TJ` IT Department · *IT-avdelningen*
    - `TJE` Archives & Registry · *Arkiv och registratur*
    - `TJA` IT Office · *IT-Stab*
    - `TJC` Operations & Infrastructure · *Drift och infrastruktur*
    - `TJD` System Management & Development · *Systemförvaltning och utveckling*
    - `TJB` User Support · *Användarstöd*
  - `TQ` KTH Innovation
  - `TR` KTH Library · *KTH Biblioteket*
    - `TRAB` Library Services & Learning Support · *Biblioteksservice och lärandestöd*
    - `TRAA` Operational Support & Development · *Stöd och utveckling*
    - `TRAC` Publication Infrastructure & Media · *Publiceringens infrastruktur och media*
  - `TS` Open Lab · *Open lab*
  - `TH` Research Support Office · *Avdelningen för forskningsstöd*
    - `THAB` Civil Law & Contracts Office · *Affärsjuridik*
    - `THAC` Development Office · *Development office*
    - `THAD` Research Funding · *Forskningsfinansiering*
    - `THAA` Research Support Office · *Forskningsstöd - Gemensamma projekt* <!-- check: shared or service unit, does it need its own category? -->
    - `THAE` Strategic Initiatives & Collaboration · *Strategiska initiativ*
  - `TT` SciLifeLab Administration · *SciLifeLab administration*
    - `TTAB` Campus Solna
  - `TC` Security & Safety Department · *Säkerhetsavdelningen*
  - `TK` Sustainability, Real Estate & Facility Service · *Fastighetsavdelningen*
    - `TKAE` Custodial Services · *Lokalvård*
    - `TKAC` KTH Sustainability Office · *KTH Sustainability office*
    - `TKAF` Maintenance Services · *Hantverksgruppen*
    - `TKAG` Property Department Office · *Kansli*
    - `TKAA` Real Estate · *Fastigheter*
  - `TL` University Administration ABE · *ABE verksamhetsstöd*
    - `TLAD` ABE Student Affairs · *Utbildningskansli ABE*
    - `TLAG` Finance ABE · *Ekonomi ABE*
    - `TLAB` Management & Researcher Support · *Lednings- och forskarstöd*
    - `TLAA` Management Office ABE · *Ledningskansli ABE*
    - `TLAC` Service & Event · *Service och event*
  - `TM` University Administration CBH · *CBH Verksamhetsstöd*
    - `TMAB` CBH Education Office · *Utbildningskansli CBH*
    - `TMAE` CBH Infrastructure · *Infrastruktur CBH*
    - `TMAA` CBH Management · *Ledningskansli CBH*
    - `TMAF` Finance CBH · *Ekonomi CBH*
  - `TN` University Administration EECS · *EECS Verksamhetsstöd*
    - `TNU` EECS Student Affairs · *Utbildningskansli EECS*
    - `TNAE` Finance EECS · *Ekonomi EECS*
    - `TNI` Infrastructure & service EECS · *Infra- och serviceenheten EECS*
    - `TNAA` Manangement Office EECS · *Ledningskansli EECS*
  - `TO` University Administration ITM · *ITM Verksamhetsstöd*
    - `TOAE` Finance ITM · *Ekonomi ITM*
    - `TOA` ITM Management · *Ledningsstöd ITM*
    - `TOD` ITM Service · *Service ITM*
    - `TOE` ITM Student Affairs · *Utbildningskansli ITM*
  - `TV` University Administration SCI · *SCI Verksamhetsstöd*
    - `TVAE` Finance SCI · *Ekonomi SCI*
    - `TVLE` SCI Albanova Service · *Albanova lokalservice Sci*
    - `TVLA` SCI Physics Administration · *Service och infrastruktur*
    - `TVAA` SCI School office · *Skolkansli SCI*
    - `TVAB` SCI Student Affairs · *Utbildningskansli SCI*
  - `TF` University Management Office · *Ledningskansliet*
    - `TFAB` Administrative Law · *Förvaltningsjuridik*
    - `TFAC` HR Management Support · *Lednings- och beslutsstöd*
    - `TFAA` University Management Office · *Planering och utveckling* <!-- check: same name as its department, merge with it? -->
- Research Centres · *Forskningscentrum*
  - Additive Manufacturing for the Life Sciences (AddLife) (UU)
  - Advanced Chip Technology (ACT) (huvudman LU)
  - Advanced Computing for Sustainable Thermal Management in Industry (AdTherm) (LU)
  - Swedish Wireless Innovation Network (SweWIN)
  - PLENTY
  - BioGlue-Centre: Competence Centre for Bio-based Adhesives
  - Academic-industrial Nuclear technology Initiative to Achieve a sustainable energy future
  - Batteries Sweden (BASE) (UU)
  - Centre for Future Seafood, Blue Food
  - Center for the Advancement of Integrated Medical and Engineering Sciences (AIMES)
  - Center for Mechanics and Material Design (MMD)
  - Centre for Design and Management of Manufacturing Systems (DMMS)
  - Center for X-rays in Swedish material science (CeXS)
  - Centre of Excellence for Science and Innovation Studies (CESIS)
  - Centre X (KTH)
  - Centre for Cyber Defence and Information Security (CDIS)
  - SUNRISE (Sustainable Nuclear Energy Research In Sweden)
  - Centre for Medical Radiation Science
  - Center for Swedish Batteries - An Alliance for Ultrahigh Performance Batteries
  - Competence Centre for Advanced BioProduction by Continuous Processing (AdBIOPRO)
  - Dig-IT Lab Sustainable Industry (Dig-IT)
  - Digital Futures (DF)
  - KTH Center for total defence
  - KTH Environmental Humanities Laboratory
  - KTH Space Center
  - Sustainable Mobile Autonomous and Resilient 6G SatCom (SMART 6G SAT)
  - Sustainable Finance Lab (SFL)
  - Svenskt förgasningscentrum (SCF)
  - Svenskt vattenkraftscentrum (SVC)
  - Swedish Electromobility Centre (SEC)
  - Swedish e-Science Research Centre (SeRC)
  - Svenskt Kärntekniskt Centrum (SKC)
  - Swedish Aerospace Physiology Centre (SAPC)
  - Swedish Life Cycle Center (SLCC)
  - Swedish Maritime Robotics Centre (SMaRC)
  - Treesearch - Collaboration on the research on new materials from the forest
  - Trustworthy Edge Computing Systems and Applications (TECoSA)
  - Wallenberg AI, Autonomous Systems and Software Program (WASP)
  - Wallenberg Wood Science Centre (WWSC)
- Sandbox · *Sandlåda* <!-- open to everyone, for trying things out -->
<!-- tree:end -->
