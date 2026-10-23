"""Finds which health, pharma, biotech and health-tech companies publish a public Greenhouse, Lever or Ashby job board.
Probes company-name guesses against the public board APIs (the same endpoints employers publish for this purpose) and
writes companies.json. Run: python3 jobsearch/discover_boards.py"""
import json, re, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import requests

HERE = Path(__file__).resolve().parent
S = requests.Session()
S.headers["User-Agent"] = "Mozilla/5.0 (personal job search; contact via repo owner)"
CA = "/root/.ccr/ca-bundle.crt"
if Path(CA).exists():
    S.verify = CA

NAMES = """Flatiron Health;Tempus;Komodo Health;Doximity;Zocdoc;Included Health;Ro;Hims & Hers;Cityblock Health;Color Health;Headway;Spring Health;Maven Clinic;Oscar Health;Devoted Health;Capsule;Alto Pharmacy;Truepill;Nomi Health;Curology;23andMe;Recursion;Benchling;Schrodinger;Relay Therapeutics;Insitro;Invitae;Guardant Health;Natera;Grail;Freenome;CareDx;Veracyte;Butterfly Network;Olive AI;Sword Health;Hinge Health;Omada Health;Lyra Health;Noom;Medisafe;GoodRx;Cost Plus Drugs;Honeybee Health;Amwell;OpenEvidence;Pearl Health;Science 37;Medidata;Veeva;Certara;Lindus Health;Phesi;Doceree;Arcadia;Health Catalyst;Innovaccer;Carbon Health;One Medical;Parsley Health;Everlywell;Ginger;Teladoc;Livongo;Virta Health;Dario Health;Biofourmis;Cadence;Cerebral;Done Global;Brightside;Ophelia;Folx Health;Thirty Madison;Wheel;Sesame Care;Zus Health;Particle Health;Redox;Health Gorilla;Ribbon Health;Commure;Abridge;Ambience Healthcare;Suki;Nabla;Tennr;Notable Health;Qventus;Cohere Health;Rocket Pharmacy;Mark Cuban;SmithRx;Capital Rx;Judi Health;Prime Therapeutics;RxSense;Rightway;Navitus;Waltz Health;Trial Pay;Medable;Clinical Ink;Veeva Systems;Verana Health;Aetion;Evidation;Datavant;Truveta;Ontada;PicnicHealth;Reify Health;Antidote;Citeline;Medidata Solutions;ObvioHealth;Thread Research;Curebase;Lightship;Formation Bio;Eli Lilly;Moderna;BioNTech;Illumina;Genentech;Gilead;Vertex;Regeneron;Alnylam;Biogen;Sarepta;Ionis;Neurocrine;Exelixis;Incyte;BridgeBio;Revolution Medicines;Arcellx;Cytokinetics;Intellia;CRISPR Therapeutics;Editas;Beam Therapeutics;Verve Therapeutics;Prime Medicine;Ginkgo Bioworks;Zymergen;Twist Bioscience;Adaptive Biotechnologies;10x Genomics;Pacific Biosciences;Personalis;Sema4;GeneDx;Myriad Genetics;Exact Sciences;Quanterix;Seer;Inscripta;Absci;Generate Biomedicines;Atomwise;Exscientia;Valo Health;BenevolentAI;Isomorphic;Owkin;Sanofi;Bayer;Novo Nordisk;AstraZeneca;GSK;Pfizer;Merck;Roche;Takeda;Teva;Viatris;Sandoz;Hikma;Zentiva;Orion Pharma;Ipsen;UCB;Lundbeck;Grifols;Almirall;Chiesi;Menarini;Servier;Pierre Fabre;Stada;Cipla;Dr Reddys;Sun Pharma;Lupin;Zydus;Aurobindo;Ergomed;PrimeVigilance;Syneos Health;ICON;IQVIA;Parexel;PPD;Fortrea;Medpace;Premier Research;Worldwide Clinical Trials;Precision for Medicine;Clinipace;Novotech;Caidya;Cmed;Pharmalex;Arriello;Qinecsa;Drug Safety Alliance;Oxford PharmaGenesis;Syneos;Cencora;AmerisourceBergen;McKesson;Cardinal Health;Walgreens;CVS Health;Express Scripts;Optum;Elevance;Humana;Centene;Cigna;Bright Health;Clover Health;Alignment Healthcare;Oak Street Health;Agilon;ChenMed;Cano Health;VillageMD;Privia;Aledade;Evolent;Signify Health;Accolade;Transcarent;Hello Heart;Pager Health;Reflexion;Kaia Health;Sword;Hinge;Quit Genius;Pelago;Calm;Headspace;Talkspace;Rula;Lyra;Modern Health;Ginger.io;Grow Therapy;Alma;Brightline;Mindstrong;Woebot;Akili;Pear Therapeutics;Propeller Health;Biobeat;Withings;Oura;Whoop;Dexcom;Insulet;Tandem Diabetes;Abbott;Medtronic;Boston Scientific;Intuitive;Hologic;ResMed;Masimo;Align;Zimmer Biomet;Stryker;Edwards Lifesciences;Natus;Nuvectra;Cerner;Epic;athenahealth;Elation Health;Healthie;Canvas Medical;Akute Health;Dr Chrono;Practice Fusion;ModMed;NextGen;Greenway;eClinicalWorks;Kareo;Tebra;AdvancedMD;CureMD;Azalea Health;Medecision;HealthEdge;Zelis;Cedar;Waystar;R1 RCM;Ensemble Health;Experian Health;Change Healthcare;Availity;Inovalon;Lumeris;Clarify Health;Komodo;Definitive Healthcare;Veradigm;IQVIA Biotech;Healx;Medicines for Europe;Clinigen;Alcami;Catalent;Lonza;Thermo Fisher;Charles River;Labcorp;Quest Diagnostics;Syneos Health Commercial;Indegene;Genpact;Cognizant;ProPharma;Pharmaceutical Product Development;Emmes;Cytel;Veristat;Pharmaron;WuXi;Evotec;Bicycle Therapeutics;Autolus;Achilles Therapeutics;Immunocore;Exscientia;Oxford Nanopore;Genomics England;Congenica;Huma;Babylon Health;Kry;Livi;Doctolib;Alan;Qare;Doctorlib;Medwing;Ada Health;Mediktor;Zava;Pharmacy2U;Boots;Lloyds Pharmacy;Well Pharmacy;Echo Pharmacy;Medicspot;Numan;Juniper;Voy;Eucalyptus;Pillar;Dispatch Health;Zipdrug;Medly Pharmacy;Blink Health;SingleCare;Amazon Pharmacy;PillPack;Capsule Pharmacy;Alto;NowRx;Genoa Healthcare;Omnicell;Parata;ScriptPro;BD;Pyxis;Swisslog Healthcare;Rx.com;Spokane;Pharmacy Quality Solutions;Surescripts;CoverMyMeds;NCPDP;DrFirst;Updox;Phreesia;Luma Health;Solutionreach;Klara;Artera;Weave;Zocdoc Inc;ShiftMed;IntelyCare;Trusted Health;Vivian Health;Aya Healthcare;Medely;Nomad Health;CareRev;Clipboard Health;Incredible Health;Hospitalists Now;Doximity Inc;Sermo;Figure 1;Amboss;Osmosis;Lecturio;Medscape;WebMD;Healthline;Drugs.com;Epocrates;Lexicomp;Wolters Kluwer;Elsevier;Clarivate;Springer Nature;Cochrane;Evidera;PharmaLex;Syneos One;Cello Health;Havas Health;Ogilvy Health;Publicis Health;Fingerpaint;Everest Clinical;ClinChoice;Linical;Ividata;Amarex;Rho;Axiom Real-Time Metrics;Alira Health;Lumanity;Putnam;Costello Medical;Complete HEOR;Maverex;Triducive;Remedy Health;Healthwise;Wellframe;Wellbeing Partners;Sharecare;Livongo Health;Vida Health;Onduo;Welldoc;Glooko;Steady Health;Twin Health;Nutrisense;Levels;Lark Health;Diabeloop;Ypsomed;Embecta;Senseonics;Biolinq""".split(";")
NAMES = list(dict.fromkeys(n.strip() for n in NAMES if n.strip()))

def variants(name):
    base = re.sub(r"[^a-z0-9 &.-]", "", name.lower())
    nospace = re.sub(r"[^a-z0-9]", "", base)
    hyph = re.sub(r"[^a-z0-9]+", "-", base).strip("-")
    short = re.sub(r"\b(inc|health|pharma|pharmaceuticals|therapeutics|bio|biosciences|systems|solutions|group)\b", "", base).strip()
    short = re.sub(r"[^a-z0-9]", "", short)
    return list(dict.fromkeys(v for v in (nospace, hyph, short) if v and len(v) > 1))

def probe(args):
    name, slug = args
    out = []
    try:
        r = S.get(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs", timeout=15)
        if r.status_code == 200 and r.json().get("jobs") is not None:
            out.append(("greenhouse", slug, name, len(r.json()["jobs"])))
    except Exception:
        pass
    try:
        r = S.get(f"https://api.lever.co/v0/postings/{slug}", params={"mode": "json"}, timeout=15)
        if r.status_code == 200 and isinstance(r.json(), list) and r.json():
            out.append(("lever", slug, name, len(r.json())))
    except Exception:
        pass
    try:
        r = S.get(f"https://api.ashbyhq.com/posting-api/job-board/{slug}", timeout=15)
        if r.status_code == 200 and r.json().get("jobs"):
            out.append(("ashby", slug, name, len(r.json()["jobs"])))
    except Exception:
        pass
    time.sleep(0.05)
    return out

def main():
    todo = [(n, v) for n in NAMES for v in variants(n)]
    found = {}
    with ThreadPoolExecutor(8) as ex:
        for res in ex.map(probe, todo):
            for ats, slug, name, n in res:
                found[(ats, slug)] = {"ats": ats, "slug": slug, "company": name, "openings": n}
    rows = sorted(found.values(), key=lambda r: (r["company"].lower(), r["ats"]))
    (HERE / "companies.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
    print(len(todo), "probes;", len(rows), "boards found")
    for r in rows:
        print(r["ats"], r["slug"], "|", r["company"], r["openings"])

if __name__ == "__main__":
    main()
