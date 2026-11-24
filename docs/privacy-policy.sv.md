# Integritetspolicy för en Indico-tjänst: utkast (svenska)

> **Status: utkast, ej fastställt.** Detta är en utgångspunkt för integritetspolicyn för en
> Indico-tjänst vid ett lärosäte, inte juridisk rådgivning; låt dataskyddsombudet granska den.
> Text inom `{{…}}` ska ersättas; *[kursiva anvisningar inom hakparentes]* tas bort före
> publicering. Den engelska versionen är `privacy-policy.en.md`; håll dem i takt.
>
> Strukturen följer den mall för integritetsmeddelanden som SWAMID ber tjänsteleverantörer
> publicera (bygger på GÉANT Data Protection Code of Conduct). Stäm av rubrikerna mot SWAMID:s
> aktuella mall vid registreringen.
>
> Indico-funktionerna som nämns är kontrollerade mot Indico v3.3.14.

---

## 1. Tjänstens namn

{{SERVICE_NAME}}, på {{SERVICE_URL}}.

## 2. Beskrivning av tjänsten

{{SERVICE_NAME}} är {{ORGANISATION}}s system för möten, seminarier och konferenser, byggt på
[Indico](https://getindico.io), öppen källkod utvecklad vid CERN. Här finns agendor,
mötesanteckningar, presentationsmaterial, anmälningar och deltagarlistor. Tjänsten drivs av
{{ORGANISATION}} på egna servrar.

## 3. Personuppgiftsansvarig och kontakt

- **Personuppgiftsansvarig:** {{ORGANISATION}}, {{ORG_ADDRESS}}, organisationsnummer
  {{ORG_NUMBER}}.
- **Kontakt för tjänsten:** {{SERVICE_CONTACT_EMAIL}}. *[Använd en funktionsadress, inte en
  person.]*
- **Dataskyddsombud:** {{DPO_EMAIL}}.

**Evenemang med andra arrangörer.** Som standard är {{ORGANISATION}} personuppgiftsansvarig
för allt i tjänsten. När ett evenemang anordnas tillsammans med en annan organisation kan
evenemangets egen sida *Integritet* ange ytterligare eller annan personuppgiftsansvarig och länka
till den organisationens policy. Den informationen gäller då evenemangets anmälningsuppgifter.
*[Stryk stycket om samarrangemang inte stöds.]*

## 4. Jurisdiktion och tillsynsmyndighet

{{COUNTRY_CODE}}. Tillsynsmyndighet: {{SUPERVISORY_AUTHORITY}}
*[Sverige: Integritetsskyddsmyndigheten (IMY), imy.se]*.

## 5. Personuppgifter som behandlas

**Från din hemorganisation när du loggar in via {{FEDERATION}}:**
- en beständig användaridentitet;
- namn;
- e-postadress;
- anknytning (t.ex. *anställd* eller *student*) med organisationens domän.

*[Anpassa listan till de attribut tjänsten faktiskt begär, t.ex. REFEDS Research and Scholarship.]*

**Från {{ORGANISATION}}s katalog**, endast för anställda vid {{ORGANISATION}}: tillhörighet till
organisatoriska enheter och grupper, för behörighetsstyrning. *[Endast om katalogintegrationen
används.]*

**Från dig eller arrangörer:**
- din profil: titel, organisation, och frivilligt telefon, adress och bild;
- svar i anmälningsformulär, som skiljer sig per evenemang;
- din roll som talare, ordförande, författare eller deltagare;
- anteckningar, dokument och annat material som laddas upp till evenemang.

**Skapas av tjänsten:**
- inloggningstider;
- en logg över ändringar i evenemang;
- webbserverloggar: IP-adress, tid och begärd sida.

## 6. Ändamål

Att tillhandahålla tjänsten: inloggning och behörigheter, att organisera och publicera möten och
evenemang, hantera anmälningar och skicka aviseringar. Loggar används för säkerhet och
felsökning.

**Rättslig grund:** {{LEGAL_BASIS}} *[För ett svenskt statligt lärosäte: uppgift av allmänt
intresse, art. 6.1 e GDPR.]*

## 7. Vem kan se dina uppgifter

- **Inloggade användare** kan söka efter andra användare. En sökträff visar namn, titel,
  e-postadress, organisation och profilbild. Själva profilsidan ser bara du och administratörer.
  *[Beskriv er inställning här: Indicos `ALLOW_PUBLIC_USER_SEARCH`.]*
- **Personer i ett evenemang:** talare, ordförande och författare visas med namn och organisation
  för alla som kan se evenemanget.
- **Deltagarlistor** visas bara om arrangören publicerar dem. Om arrangören ber om samtycke visas
  bara de som har samtyckt.
- **Evenemangsansvariga** ser anmälningarna till sina evenemang.
- **Skyddade kategorier och evenemang** syns bara för de personer och grupper som fått behörighet.
- **Administratörer** av tjänsten kan se alla uppgifter.

## 8. Tredje parter och överföringar

- **E-postleverans:** {{MAIL_PROVIDER}}. *[Om leverantören finns utanför EU/EES: ange land och
  överföringsgrund.]*
- **Videomöten:** om ett evenemang använder Zoom-integrationen skickas mötets titel och tid samt
  värdens identitet till Zoom, enligt {{ORGANISATION}}s avtal med Zoom. Om arrangören aktiverar
  automatisk registrering skickas även anmäldas namn och e-postadresser. *[Stryk om det inte
  används.]*
- **Profilbilder:** {{GRAVATAR_SENTENCE}} *[Om Gravatar är aktiverat: "Väljer du en
  Gravatar-bild hämtar din webbläsare den från gravatar.com med en hash av din e-postadress." Om
  avstängt (`DISABLE_GRAVATAR = True`): stryk punkten.]*

Uppgifterna säljs inte och används inte för marknadsföring.

## 9. Lagringstid

- **Evenemangsinnehåll** (agendor, talare, anteckningar, material) sparas så länge evenemanget
  finns. Det är en del av {{ORGANISATION}}s dokumentation av verksamheten och omfattas av
  {{RECORDS_RULES}}. *[Ange vilka arkiv- och gallringsregler som gäller, eller att frågan utreds.]*
- **Anmälningar:** varje anmälningsformulär har en lagringstid som arrangören anger, högst
  {{MAX_REGISTRATION_RETENTION}}. Därefter raderas anmälningarna.
- **Konton:**
  - ett konto utan inloggning på {{BLOCK_AFTER}} spärras: det kan inte logga in, syns inte i
    sökningar och sparas så att det kan återaktiveras;
  - efter {{ANONYMISE_AFTER}} utan inloggning anonymiseras kontot.
  - Ditt namn står kvar i agendor där du varit talare eller författare, om du inte begär att det
    tas bort.
- **Webbserverloggar:** {{LOG_RETENTION}}.
- **Säkerhetskopior:** {{BACKUP_RETENTION}}. Raderade uppgifter försvinner ur säkerhetskopiorna
  när dessa löper ut.

## 10. Dina rättigheter

Du har rätt att:
- få tillgång till dina uppgifter, och att själv exportera dem (*Min profil → Data export*);
- få dem rättade eller raderade;
- invända mot behandlingen;
- klaga hos tillsynsmyndigheten.

Skicka begäran till {{REQUESTS_CONTACT}}. Visst innehåll kan behöva bevaras enligt de regler om
allmänna handlingar och arkiv som gäller för {{ORGANISATION}}.

## 11. Uppförandekod för dataskydd

Personuppgifter från din hemorganisation skyddas enligt
[GÉANT Data Protection Code of Conduct](https://wiki.refeds.org/display/CODE/Data+Protection+Code+of+Conduct+Home).
*[Behåll bara om tjänsten deklarerar efterlevnad i federationen.]*

---

Senast ändrad: {{DATE}}
