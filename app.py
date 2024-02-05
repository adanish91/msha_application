from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.MORPH, dbc_css])

df = pd.read_csv("Accidents.txt", delimiter='|', encoding='ISO-8859-1', low_memory=False)
mines = pd.read_csv("mines.txt", delimiter='|', encoding='ISO-8859-1', low_memory=False)
violations = pd.read_csv("violations.txt", delimiter='|', encoding='ISO-8859-1', low_memory=False)

load_figure_template("MORPH")

min_to_display = list(df["SUBUNIT"].unique())
years_to_display = list(range(df["CAL_YR"].min(), df["CAL_YR"].max() + 1, 1))
marks_year = {year: {'label': str(year), 'style': {'font-size': '10px'}} for year in
              range(df["CAL_YR"].min(), df["CAL_YR"].max() + 1)}
marks_mining = {m_type: str(m_type) for m_type in min_to_display}

mining_type_options = [{'label': 'Mill operations', 'value': 'MILL OPERATION/PREPARATION PLANT'},
                       {'label': 'Surface', 'value': 'STRIP, QUARY, OPEN PIT'},
                       {'label': 'Underground', 'value': 'UNDERGROUND'},
                       {'label': 'Surface at UG', 'value': 'SURFACE AT UNDERGROUND'},
                       {'label': 'Dredge', 'value': 'DREDGE'},
                       {'label': 'Auger', 'value': 'AUGER'},
                       {'label': 'Office workers', 'value': 'OFFICE WORKERS AT MINE SITE'},
                       {'label': 'Other mining', 'value': 'OTHER MINING'},
                       {'label': 'Shops/Yards', 'value': 'INDEPENDENT SHOPS OR YARDS'},
                       {'label': 'Culm/Refuse pile', 'value': 'CULM BANK/REFUSE PILE'}]

coal_metal_options = [{'label': 'Metal', 'value': 'M'},
                      {'label': 'Coal', 'value': 'C'}]

states_options = ['AL', 'KY', 'TN', 'GA', 'WV', 'PA', 'IL', 'AZ', 'MT', 'CA', 'NV',
                  'TX', 'AR', 'MS', 'OK', 'ND', 'OR', 'CO', 'SD', 'NM', 'WY', 'KS',
                  'UT', 'CT', 'DE', 'FL', 'ID', 'WA', 'IN', 'MI', 'OH', 'IA', 'MN',
                  'WI', 'MO', 'NE', 'VA', 'LA', 'ME', 'NH', 'MD', 'MA', 'VT', 'NJ',
                  'NY', 'NC', 'SC', 'RI', 'AK', 'HI', 'PR', 'VI', 'AS', 'GU', 'MP']

degree_injury_options = [{'label': 'Days Restricted Activity Only', 'value': 'DAYS RESTRICTED ACTIVITY ONLY'},
                         {'label': 'Days Away From Work Only', 'value': 'DAYS AWAY FROM WORK ONLY'},
                         {'label': 'No Days Away & No Restricted Activity', 'value': 'NO DYS AWY FRM WRK,NO RSTR ACT'},
                         {'label': 'Days Away & Restricted Activity', 'value': 'DYS AWY FRM WRK & RESTRCTD ACT'},
                         {'label': 'Permanent Disability', 'value': 'PERM TOT OR PERM PRTL DISABLTY'},
                         {'label': 'Accidents Only', 'value': 'ACCIDENT ONLY'},
                         {'label': 'Occupational Illness', 'value': 'OCCUPATNAL ILLNESS NOT DEG 1-6'},
                         {'label': 'No Value', 'value': 'NO VALUE FOUND'},
                         {'label': 'Fatality', 'value': 'FATALITY'},
                         {'label': 'All Other Cases', 'value': 'ALL OTHER CASES (INCL 1ST AID)'},
                         {'label': 'Injuries Due To Natural Cause', 'value': 'INJURIES DUE TO NATURAL CAUSES'},
                         {'label': 'Injuries Involving Non-Employees', 'value': 'INJURIES INVOLVNG NONEMPLOYEES'}]

injury_source_options = [{'label': 'Metal (pipe, wire, nail)', 'value': 'METAL,NEC(PIPE,WIRE,NAIL)'},
                         {'label': 'Broken rock/coal/ore/waste', 'value': 'BROKEN ROCK,COAL,ORE,WSTE'},
                         {'label': 'Ladders', 'value': 'LADDERS,NEC'},
                         {'label': 'Barrels/kegs/drums', 'value': 'BARRELS,KEGS,DRUMS'},
                         {'label': 'Nonpowered Handtools', 'value': 'HAND TOOLS,NONPOWERED,NEC'},
                         {'label': 'Ground', 'value': 'GROUND'},
                         {'label': 'Floor/walking surface not UG', 'value': 'FLOOR,WALKING SURF-NOT UG'},
                         {'label': 'Pallets', 'value': 'PALLETS'},
                         {'label': 'Pulverize mineral (Dust)', 'value': 'PULVERIZED MINERAL (DUST)'},
                         {'label': 'Motors', 'value': 'MOTORS'},
                         {'label': 'Crowbar/pry bar', 'value': 'CROWBAR,PRY BAR'},
                         {'label': 'Steps', 'value': 'STEPS'},
                         {'label': 'Chute/slide-converyer hoper', 'value': 'CHUTE & SLIDE-CONVYR HOPR'},
                         {'label': 'Electrical apparatus', 'value': 'ELECTRICAL APPARATUS,NEC'},
                         {'label': 'Boiler/pressure vessel/air hose/ox', 'value': 'BOILR,PRES VSL,AIR HOS,OX'},
                         {'label': 'Belt Conveyors', 'value': 'BELT CONVEYORS'},
                         {'label': 'Heat (Environment)', 'value': 'HEAT (ATMOS + ENVIRON)'},
                         {'label': 'Metal covers/guards', 'value': 'METAL COVERS & GUARDS'},
                         {'label': 'Kiln prod/Inc build up removal', 'value': 'KILN PROD,INC BLDUP,REMOV'},
                         {'label': 'Mine floor/bottom/footwall', 'value': 'MINE FLOOR,BOTTOM,FOOTWAL'},
                         {'label': 'Bags', 'value': 'BAGS'},
                         {'label': 'Mine Jeep/kersey/jitney', 'value': 'MINE JEEP,KERSEY,JITNEY'},
                         {'label': 'Miscellaneous', 'value': 'MISCELLANEOUS,NEC'},
                         {'label': 'Underground mining machines', 'value': 'UNDERGRD MINING MACHINES'},
                         {'label': 'Acid/alkali/wet cement', 'value': 'ACIDS,ALKALI,WET CEMENT'},
                         {'label': 'Caving rock/coal/ore/waste', 'value': 'CAVING ROCK,COAL,ORE,WSTE'},
                         {'label': 'Roof (rock) bolts', 'value': 'ROOF (ROCK) BOLTS'},
                         {'label': 'Post/caps/headers/timber', 'value': 'POST,CAPS,HEADERS,TIMBER'},
                         {'label': 'Boxes/crates/cartons', 'value': 'BOXES,CRATES,CARTONS'},
                         {'label': 'Steel rail', 'value': 'STEEL RAIL (ALL KINDS)'},
                         {'label': 'Blocking', 'value': 'BLOCKING'},
                         {'label': 'Longwall support/chock', 'value': 'LONGWALL SUPT,JKS & CHOCK'},
                         {'label': 'Coal/petrol product', 'value': 'COAL & PETROL PRODUCT,NEC'},
                         {'label': 'Knife', 'value': 'KNIFE'},
                         {'label': 'Surface mining machines', 'value': 'SURFACE MINING MACHINES'},
                         {'label': 'Wrench', 'value': 'WRENCH'},
                         {'label': 'Drill steel', 'value': 'DRILL STEEL (ALL SIZES)'},
                         {'label': 'Cranes/derricks', 'value': 'CRANES,DERRICKS'},
                         {'label': 'Conductor/electric/cable', 'value': 'CONDCTR,ELCT,CBL,TROL POL'},
                         {'label': 'Doors/UG ventilation', 'value': 'DOORS,INCL UG VENTILATION'},
                         {'label': 'Axe/hammer/sledge', 'value': 'AXE,HAMMER,SLEDGE'},
                         {'label': 'Wood items', 'value': 'WOOD ITEMS,NEC'},
                         {'label': 'Animals/insects/birds/reptile', 'value': 'ANIMALS,INSCTS,BRDS,REPTL'},
                         {'label': 'Nonpowered vehicles', 'value': 'NONPOWRD VECH-DOLI,WHLBRW'},
                         {'label': 'Stairs/steps outside', 'value': 'STAIRS,STEPS-OUTSIDE'},
                         {'label': 'Machine-mill/cleaning plant', 'value': 'MACHINE-MILL,CLEANING PLT'},
                         {'label': 'Rail Car surface equipment', 'value': 'STD G RAIL CR,MTR-SURF EQ'},
                         {'label': 'Noise', 'value': 'NOISE,NEC'},
                         {'label': 'Pumps/fans/comp/eng', 'value': 'PUMPS,FANS,COMP,ENG,NEC'},
                         {'label': 'Loose dirt/mud', 'value': 'LOOSE DIRT AND MUD'},
                         {'label': 'Mineral items', 'value': 'MINERAL ITEMS,NEC'},
                         {'label': 'Cars/pickup trucks', 'value': 'PASS CARS,PICKUP TRUCKS'},
                         {'label': 'Powered handtools', 'value': 'HAND TOOLS,POWERED,NEC'},
                         {'label': 'Bodily motion', 'value': 'BODILY MOTION'},
                         {'label': 'Chain/rope/cable', 'value': 'CHAIN,ROPE,CABLE-NT CONVY'},
                         {'label': 'Wheel grinder', 'value': 'ABRAS STONE,WHEEL GRINDER'},
                         {'label': 'Machine/welder', 'value': 'MACHINE,NEC-WELDR,OFC MAC'},
                         {'label': 'Transformers/converters', 'value': 'TRANSFORMERS,CONVERTERS'},
                         {'label': 'Ice', 'value': 'ICE'},
                         {'label': 'Conveyors', 'value': 'CONVEYORS,NEC'},
                         {'label': 'Storage tanks & bins', 'value': 'STORAGE TANKS AND BINS'},
                         {'label': 'Moveable ladders', 'value': 'MOVEABLE LADDERS'},
                         {'label': 'Forklifts/stackers/tractor', 'value': 'FORKLIFTS,STACKERS,TRCTR'},
                         {'label': 'Chemicals/chemical compounds', 'value': 'CHEMICALS,CHEM COMP,NEC'},
                         {'label': 'Containers', 'value': 'CONTAINERS,NEC'},
                         {'label': 'Cement/concrete block', 'value': 'CEMENT PROD,CONCRET BLOCK'},
                         {'label': 'Brick/ceramic', 'value': 'BRICK,CERAMIC'},
                         {'label': 'Molten metal', 'value': 'MOLTEN METAL'},
                         {'label': 'Power saw', 'value': 'POWER SAW'},
                         {'label': 'Working surface outside', 'value': 'WORKING SURF OUTSIDE,NEC'},
                         {'label': 'Apparel', 'value': 'APPAREL,NEC'},
                         {'label': 'Dam/locks/ponds/bridges', 'value': 'DAMS,LOCKS,PONDS,BRIDGES'},
                         {'label': 'Building/structure/boat/raft', 'value': 'BLDG,STRUCT,BOAT,RAFT,NEC'},
                         {'label': 'Mine rescue equipment', 'value': 'MINE RESCUE EQUIPMENT'},
                         {'label': 'Drum/puly/sheave-nt conveyor', 'value': 'DRUM,PULY,SHEAVE-NT CONVY'},
                         {'label': 'Water', 'value': 'WATER'},
                         {'label': 'Drill percussion/hard rock/jackhammer', 'value': 'DRIL-PRCUSV,HRD ROC,JKHMR'},
                         {'label': 'Mechanical/hydraulic/air jacks', 'value': 'JACKS-MECH,HYDRL,AIR,ETC'},
                         {'label': 'Sand/gravel/shell', 'value': 'SAND,GRAVEL,SHELL'},
                         {'label': 'Rib/side', 'value': 'SIDE OR RIB'},
                         {'label': 'Wheel-from car/truck', 'value': 'WHEEL-FROM CAR OR TRUCK'},
                         {'label': 'Hoisting apparatus', 'value': 'HOISTING APPARATUS,NEC'},
                         {'label': 'Towers/poles', 'value': 'TOWERS,POLES,ETC'},
                         {'label': 'Belts(Not conveyor)', 'value': 'BELTS (NOT CONVEYOR)'},
                         {'label': 'Flame/Fire/Smoke', 'value': 'FLAME,FIRE,SMOKE,NEC'},
                         {'label': 'Mechanical power transmission', 'value': 'MCH PWR TRNSMSN APPR,NEC'},
                         {'label': 'Back/mine roof/hanging wall', 'value': 'BACK,MINE ROOF,HNGNG WALL'},
                         {'label': 'Soaps/Detergent/cleaning compound', 'value': 'SOAPS,DETER,CLN COMP,NEC'},
                         {'label': 'Fixed ladders', 'value': 'FIXED LADDERS'},
                         {'label': 'Brattice curt/plas/canv', 'value': 'BRATTICE CURT,PLAS & CANV'},
                         {'label': 'Steam', 'value': 'STEAM'},
                         {'label': 'Elevators/cages/skips', 'value': 'ELEVATORS,CAGES,SKIPS,ETC'},
                         {'label': 'Shaking/vibrating conveyor', 'value': 'SHAKING,VIBRATNG CONVEYOR'},
                         {'label': 'Street/road', 'value': 'STREET,ROAD'},
                         {'label': 'Hoist/chain block', 'value': 'CHAIN HOIST, CHAIN BLOCK'},
                         {'label': 'Noxious mine gases', 'value': 'NOXIOUS MINE GASES,NEC'},
                         {'label': 'Radiating substance of equip', 'value': 'RDIATNG SUBST OF EQIP,NEC'},
                         {'label': 'Snow', 'value': 'SNOW'},
                         {'label': 'Underground', 'value': 'UNDERGROUND,NEC'},
                         {'label': 'Railroad ties', 'value': 'RAILROAD TIES'},
                         {'label': 'Wharfs/docks', 'value': 'WHARFS,DOCKS,ETC'},
                         {'label': 'Drill/rotary (Coal drill)', 'value': 'DRILL,ROTARY (COAL DRILL)'},
                         {'label': 'Plants/trees/vegetation', 'value': 'PLANTS,TREES,VEGETATION'},
                         {'label': 'Liquids', 'value': 'LIQUIDS,NEC'},
                         {'label': 'Longwall conveyor', 'value': 'LONGWALL CONVEYOR'},
                         {'label': 'Space heaters', 'value': 'SPACE HEATERS'},
                         {'label': 'Naro g rail cr, meter-UG equipment', 'value': 'NARO G RAIL CR,MTR-UG EQP'},
                         {'label': 'Landslide', 'value': 'LANDSLIDE (SURF ONLY)'},
                         {'label': 'Mine headframe', 'value': 'MINE HEADFRAME'},
                         {'label': 'Cold (environment)', 'value': 'COLD(ATMOS,ENVIR)NEC'},
                         {'label': 'Generators', 'value': 'GENERATORS'},
                         {'label': 'Cribbing', 'value': 'CRIBBING'},
                         {'label': 'Impactor/tamper', 'value': 'IMPACTOR,TAMPER'},
                         {'label': 'Chisel', 'value': 'CHISEL'},
                         {'label': 'Kilns/melt furnace/retort', 'value': 'KILNS,MELT FURNACE,RETORT'},
                         {'label': 'Vehicles', 'value': 'VEHICLES,NEC'},
                         {'label': 'Radioactive ore radiation', 'value': 'RDIOACT ORE-INJ FM RDIATN'},
                         {'label': 'Explosive direct related to injury', 'value': 'EXPLOSIVE-DIR REL TO INJR'},
                         {'label': 'Other heating equipment', 'value': 'OTHER HEATING EQUIP,NEC'},
                         {'label': 'Methane gas mine/process', 'value': 'METHANE GAS-IN MNE & PROC'},
                         {'label': 'Electric hoist', 'value': 'ELECTRIC HOIST'},
                         {'label': 'Air hoist', 'value': 'AIR HOIST'},
                         {'label': 'Coal (processed)', 'value': 'COAL (PROCESSED)'},
                         {'label': 'Oxygen deficient atmosphere', 'value': 'OXYGEN DEFICIENT ATMOSPHR'},
                         {'label': 'Scaffolds/staging', 'value': 'SCAFFOLDS,STAGING,ETC'},
                         {'label': 'No Values', 'value': 'NO VALUE FOUND'},
                         {'label': 'Highway ore carrier', 'value': 'HGHWY ORE CARIER,LRGE TRK'},
                         {'label': 'Rubber/Glass/Plastic/Fiberglass', 'value': 'RBR,GLS,PLSTC,FIBRGLS,FAB'},
                         {'label': '100', 'value': '100'},
                         {'label': '160', 'value': '160'},
                         {'label': '170', 'value': '170'},
                         {'label': '180', 'value': '180'},
                         {'label': '200', 'value': '200'},
                         {'label': '220', 'value': '220'},
                         {'label': '260', 'value': '260'},
                         {'label': '301', 'value': '301'},
                         {'label': '310', 'value': '310'},
                         {'label': '320', 'value': '320'},
                         {'label': '330', 'value': '330'},
                         {'label': '390', 'value': '390'},
                         {'label': '370', 'value': '370'},
                         {'label': '400', 'value': '400'},
                         {'label': 'Invalid Code', 'value': '?'}]

nature_injury_options = [{'label': 'Cut/Lacer/Puncture', 'value': 'CUT,LACER,PUNCT-OPN WOUND'},
                         {'label': 'Sprain/Strain/Rupture disc', 'value': 'SPRAIN,STRAIN RUPT DISC'},
                         {'label': 'Scratch/Abrasion', 'value': 'SCRATCH,ABRASION,SUPERFCL'},
                         {'label': 'Unclassified', 'value': 'UNCLASSIFIED,NOT DETERMED'},
                         {'label': 'Burn/Chemical-fume/compound', 'value': 'BURN,CHEMICL-FUME,COMPOUN'},
                         {'label': 'Hernia;Rupture', 'value': 'HERNIA;RUPTURE'},
                         {'label': 'Amputation/Encleation', 'value': 'AMPUTATION OR ENUCLEATION'},
                         {'label': 'Heatstroke/exhausion', 'value': 'HEATSTROK,SUNSTR,HT EXHAU'},
                         {'label': 'Contusion/Bruise/Intact skin', 'value': 'CONTUSN,BRUISE,INTAC SKIN'},
                         {'label': 'Fracture/Chip', 'value': 'FRACTURE,CHIP'},
                         {'label': 'Joint/Tendon/Muscle Inflammation', 'value': 'JOINT,TENDON,MUSCL INFLAM'},
                         {'label': 'Electric arc burn-not contact', 'value': 'ELECT.ARC BURN-NOT CONTAC'},
                         {'label': 'Other Injury', 'value': 'OTHER INJURY,NEC'},
                         {'label': 'Crushing', 'value': 'CRUSHING'},
                         {'label': 'Dust in eyes', 'value': 'DUST IN EYES'},
                         {'label': 'Multiple Injuries', 'value': 'MULTIPLE INJURIES'},
                         {'label': 'Poisoning, systemic', 'value': 'POISONING,SYSTEMIC'},
                         {'label': 'Dislocation', 'value': 'DISLOCATION'},
                         {'label': 'Hearing loss/Impairment', 'value': 'HEARING LOSS OR IMPAIRMNT'},
                         {'label': 'Concussion-Brain/Cerebral', 'value': 'CONCUSSION-BRAIN,CEREBRAL'},
                         {'label': 'Dermatitis/Rash/Skin Inflam', 'value': 'DERMATITIS,RASH,SKIN INFL'},
                         {'label': 'Burn/Scald (Heat)', 'value': 'BURN OR SCALD (HEAT)'},
                         {'label': 'Heart Attach', 'value': 'HEART ATTACK'},
                         {'label': 'Silicosis', 'value': 'SILICOSIS'},
                         {'label': 'Occupational Diseases', 'value': 'OCCUPATIONAL DISEASES,NEC'},
                         {'label': 'Pneumoconiosis/Black lung', 'value': 'PNEUMOCONIOSIS,BLACK LUNG'},
                         {'label': 'Electric Shock/Electrocution', 'value': 'ELECT SHOCK,ELECTROCUTION'},
                         {'label': 'Electric Burn-Contact', 'value': 'ELECTRIC BURN-CNTACT BURN'},
                         {'label': 'Suffocation/Smoke/Inhalation/Drown', 'value': 'SUFFOC,SMOK INHILAT,DROWN'},
                         {'label': 'Other Radiation Effect', 'value': 'OTH RADIATION EFFECT,NEC'},
                         {'label': 'Cerebral Hemorage-Not CCUS', 'value': 'CEREBRAL HEMORAGE-NT CCUS'},
                         {'label': 'Freezing/Frostbite', 'value': 'FREEZNG,FROSTBITE,LO TEMP'},
                         {'label': 'Contagious/Infectious disease', 'value': 'CONTAGIOUS,INFECT DISEASE'},
                         {'label': 'Asbestosis', 'value': 'ASBESTOSIS'},
                         {'label': 'Other Pnemoconiosis', 'value': 'OTHER PNEUMOCONIOSIS,NEC'},
                         {'label': 'Sunburn', 'value': 'SUNBURN'},
                         {'label': 'Laser Burn', 'value': 'LASER BURN'},
                         {'label': 'Lung Cancer/Ionizing Radiation', 'value': 'LUNG CANCER,IONIZNG RDATN'},
                         {'label': 'No value', 'value': 'NO VALUE FOUND'},
                         {'label': 'Invalid code', 'value': '?'},
                         {'label': '100', 'value': '100'},
                         {'label': '130', 'value': '130'},
                         {'label': '142', 'value': '142'},
                         {'label': '143', 'value': '143'},
                         {'label': '144', 'value': '144'},
                         {'label': '150', 'value': '150'},
                         {'label': '200', 'value': '200'},
                         {'label': '310', 'value': '310'},
                         {'label': '311', 'value': '311'},
                         {'label': '312', 'value': '312'},
                         {'label': '313', 'value': '313'},
                         {'label': '320', 'value': '320'},
                         {'label': '330', 'value': '330'},
                         {'label': '340', 'value': '340'},
                         {'label': '420', 'value': '420'},
                         {'label': '430', 'value': '430'},
                         {'label': '440', 'value': '440'},
                         {'label': '450', 'value': '450'},
                         {'label': '460', 'value': '460'},
                         {'label': '511', 'value': '511'},
                         {'label': '512', 'value': '512'},
                         {'label': '513', 'value': '513'},
                         {'label': '520', 'value': '520'},
                         {'label': '530', 'value': '530'},
                         {'label': '540', 'value': '540'},
                         {'label': '700', 'value': '700'}]

classification_options = [{'label': 'Machinery', 'value': 'MACHINERY'},
                          {'label': 'Handling of Materials', 'value': 'HANDLING OF MATERIALS'},
                          {'label': 'Slip/Fall', 'value': 'SLIP OR FALL OF PERSON'},
                          {'label': 'Nonpowered Haulage', 'value': 'NONPOWERED HAULAGE'},
                          {'label': 'Handtools (Nonpowered)', 'value': 'HANDTOOLS (NONPOWERED)'},
                          {'label': 'Exploding Vessels Under Pressure', 'value': 'EXPLODING VESSELS UNDER PRESSURE'},
                          {'label': 'Ignition/Explosion (Gas/Dust)', 'value': 'IGNITION OR EXPLOSION OF GAS OR DUST'},
                          {'label': 'Disorders (Physical Agents)', 'value': 'DISORDERS (PHYSICAL AGENTS)'},
                          {'label': 'Powered Haulage', 'value': 'POWERED HAULAGE'},
                          {'label': 'Fall of Roof/Back', 'value': 'FALL OF ROOF OR BACK'},
                          {'label': 'Hoisting', 'value': 'HOISTING'},
                          {'label': 'Fire', 'value': 'FIRE'},
                          {'label': 'Disorders (Repeated Trauma)', 'value': 'DISORDERS (REPEATED TRAUMA)'},
                          {'label': 'Striking/Bumping', 'value': 'STRIKING OR BUMPING'},
                          {'label': 'Electrical', 'value': 'ELECTRICAL'},
                          {'label': 'Falling/Sliding/Rolling Materials', 'value': 'FALLING/SLIDING/ROLLING MATERIALS'},
                          {'label': 'Fall of Face/Rib/Pillar/Side/Highwall',
                           'value': 'FALL OF FACE/RIB/PILLAR/SIDE/HIGHWALL'},
                          {'label': 'Stepping/Kneeling on Object', 'value': 'STEPPING OR KNEELING ON OBJECT'},
                          {'label': 'Other', 'value': 'OTHER'},
                          {'label': 'Other Occupational Illnesses', 'value': 'ALL OTHER OCCUPATIONAL ILLNESSES'},
                          {'label': 'Dust Disease of Lungs', 'value': 'DUST DISEASE OF LUNGS'},
                          {'label': 'Inundation', 'value': 'INUNDATION'},
                          {'label': 'Occupational Skin Diseases', 'value': 'OCCUPATIONAL SKIN DISEASES'},
                          {'label': 'Explosives/Breaking Agents', 'value': 'EXPLOSIVES AND BREAKING AGENTS'},
                          {'label': 'Entrapment', 'value': 'ENTRAPMENT'},
                          {'label': 'Impoundment', 'value': 'IMPOUNDMENT'},
                          {'label': 'Poisoning (Toxic Materials)', 'value': 'POISONING (TOXIC MATERIALS)'},
                          {'label': 'Respiratory Conditions (Toxic Agents)',
                           'value': 'RESPIRATORY CONDITIONS (TOXIC AGENTS)'},
                          {'label': 'No value found', 'value': 'NO VALUE FOUND'},
                          {'label': '01', 'value': '01'},
                          {'label': '02', 'value': '02'},
                          {'label': '04', 'value': '04'},
                          {'label': '05', 'value': '05'},
                          {'label': '08', 'value': '08'},
                          {'label': '12', 'value': '12'},
                          {'label': '17', 'value': '17'},
                          {'label': '18', 'value': '18'},
                          {'label': '20', 'value': '20'},
                          {'label': '21', 'value': '21'},
                          {'label': '24', 'value': '24'},
                          {'label': '27', 'value': '27'},
                          {'label': '28', 'value': '28'},
                          {'label': '30', 'value': '30'},
                          {'label': '40', 'value': '40'},
                          {'label': '44', 'value': '44'}]

injured_body_options = [
    {'label': 'Back (Muscles/spine/s-cord/tailbone)', 'value': 'BACK (MUSCLES/SPINE/S-CORD/TAILBONE)'},
    {'label': 'Arm', 'value': 'ARM,NEC'},
    {'label': 'Fingers/thumb', 'value': 'FINGER(S)/THUMB'},
    {'label': 'Jaw/Chin', 'value': 'JAW INCLUDE CHIN'},
    {'label': 'Knee/Patella', 'value': 'KNEE/PATELLA'},
    {'label': 'Shoulders (Collarbone/clavicle/scapula)', 'value': 'SHOULDERS (COLLARBONE/CLAVICLE/SCAPULA)'},
    {'label': 'Ankle', 'value': 'ANKLE'},
    {'label': 'Neck', 'value': 'NECK'},
    {'label': 'Multiple Parts', 'value': 'MULTIPLE PARTS (MORE THAN ONE MAJOR)'},
    {'label': 'Forearm/Ulnar/Radius', 'value': 'FOREARM/ULNAR/RADIUS'},
    {'label': 'Wrist', 'value': 'WRIST'},
    {'label': 'Chest (Ribs/Breastbone/Chest)', 'value': 'CHEST (RIBS/BREAST BONE/CHEST ORGNS)'},
    {'label': 'Eye/Optic Nerve/Vision', 'value': 'EYE(S) OPTIC NERVE/VISON'},
    {'label': 'Mouth/Lip/Teeth/Tongue/Throat', 'value': 'MOUTH/LIP/TEETH/TONGUE/THROAT/TASTE'},
    {'label': 'Ear(s) External', 'value': 'EAR(S) EXTERNAL'},
    {'label': 'Foot (Not Ankle/Toe)/Tarsus/Metatarsus', 'value': 'FOOT(NOT ANKLE/TOE)/TARSUS/METATARSUS'},
    {'label': 'Elbow', 'value': 'ELBOW'},
    {'label': 'Arm, Multiple parts', 'value': 'ARM, MULTIPLE PARTS'},
    {'label': 'Head', 'value': 'HEAD,NEC'},
    {'label': 'Hips (Pelvis/Organs/Kidneys/Buttocks)', 'value': 'HIPS (PELVIS/ORGANS/KIDNEYS/BUTTOCKS)'},
    {'label': 'Leg', 'value': 'LEG, NEC'},
    {'label': 'Nose/Nasal Passages/Sinus/Smell', 'value': 'NOSE/NASAL PASSAGES/SINUS/SMELL'},
    {'label': 'Upper Extremities, Multiple', 'value': 'UPPER EXTREMITIES, MULTIPLE'},
    {'label': 'Hand (Not Wrist or Fingers)', 'value': 'HAND (NOT WRIST OR FINGERS)'},
    {'label': 'Lower Leg/Tibia/Fibula', 'value': 'LOWER LEG/TIBIA/FIBULA'},
    {'label': 'Body Systems', 'value': 'BODY SYSTEMS'},
    {'label': 'Abdomen/Internal Organs', 'value': 'ABDOMEN/INTERNAL ORGANS'},
    {'label': 'Toe(s)/Phalanges', 'value': 'TOE(S)/PHALANGES'},
    {'label': 'Brain', 'value': 'BRAIN'},
    {'label': 'Lower Extremities, Multiple Parts', 'value': 'LOWER EXTREMITIES, MULTIPLE PARTS'},
    {'label': 'Face', 'value': 'FACE,NEC'},
    {'label': 'Face, Multiple Parts', 'value': 'FACE, MULTIPLE PARTS'},
    {'label': 'Thigh/Femur', 'value': 'THIGH/FEMUR'},
    {'label': 'Upper Arm/Humerus', 'value': 'UPPER ARM/HUMERUS'},
    {'label': 'Ear(s) Internal & Hearing', 'value': 'EAR(S) INTERNAL & HEARING'},
    {'label': 'Unclassified', 'value': 'UNCLASSIFIED'},
    {'label': 'Trunk, Multiple Parts', 'value': 'TRUNK, MULTIPLE PARTS'},
    {'label': 'Leg, Multiple Parts', 'value': 'LEG, MULTIPLE PARTS'},
    {'label': 'Ear(s) Internal & External', 'value': 'EAR(S) INTERNAL & EXTERNAL'},
    {'label': 'Head, Multiple Parts', 'value': 'HEAD, MULTIPLE PARTS'},
    {'label': 'Lower Extremities', 'value': 'LOWER EXTREMITIES,NEC'},
    {'label': 'Trunk', 'value': 'TRUNK,NEC'},
    {'label': 'Skull', 'value': 'SKULL'},
    {'label': 'Scalp', 'value': 'SCALP'},
    {'label': 'Upper Extremities', 'value': 'UPPER EXTREMITIES, NEC'},
    {'label': 'Body Parts, NEC', 'value': 'BODY PARTS, NEC'},
    {'label': 'No value found', 'value': 'NO VALUE FOUND'},
    {'label': '0', 'value': '0'},
    {'label': '75', 'value': '75'},
    {'label': '100', 'value': '100'},
    {'label': '235', 'value': '235'},
    {'label': '6000', 'value': '6000'},
    {'label': 'Nan', 'value': np.nan}]

accident_type_options = [{'label': 'Fall from machine', 'value': 'Fall from machine'},
                         {'label': 'Over-exertion in lifting objects', 'value': 'Over-exertion in lifting objects'},
                         {'label': 'Caught in, under or between NEC', 'value': 'Caught in, under or between NEC'},
                         {'label': 'Fall onto or against objects', 'value': 'Fall onto or against objects'},
                         {'label': 'Fall to the walkway or working surface',
                          'value': 'Fall to the walkway or working surface'},
                         {'label': 'Struck by flying object', 'value': 'Struck by flying object'},
                         {'label': 'Over-exertion NEC', 'value': 'Over-exertion NEC'},
                         {'label': 'Struck against stationary object', 'value': 'Struck against stationary object'},
                         {'label': 'Struck by... NEC', 'value': 'Struck by... NEC'},
                         {'label': 'Absorption of radiations, caustics, toxic and noxious substances',
                          'value': 'Absorption of radiations, caustics, toxic and noxious substances'},
                         {'label': 'Over-exertion in wielding or throwing objects',
                          'value': 'Over-exertion in wielding or throwing objects'},
                         {'label': 'Caught in, under or between a moving and a stationary object',
                          'value': 'Caught in, under or between a moving and a stationary object'},
                         {'label': 'Over-exertion in pulling or pushing objects',
                          'value': 'Over-exertion in pulling or pushing objects'},
                         {'label': 'Struck against a moving object', 'value': 'Struck against a moving object'},
                         {'label': 'Flash burns (welding)', 'value': 'Flash burns (welding)'},
                         {'label': 'Accident type, without injuries', 'value': 'Accident type, without injuries'},
                         {'label': 'Contact with hot objects or substances',
                          'value': 'Contact with hot objects or substances'},
                         {'label': 'Struck by falling object', 'value': 'Struck by falling object'},
                         {'label': 'Inhalation of radiations, caustics, toxic and noxious substances',
                          'value': 'Inhalation of radiations, caustics, toxic and noxious substances'},
                         {'label': 'Flash burns (electric)', 'value': 'Flash burns (electric)'},
                         {'label': 'Fall to lower level, NEC', 'value': 'Fall to lower level, NEC'},
                         {'label': 'Caught in, under or between running or meshing objects',
                          'value': 'Caught in, under or between running or meshing objects'},
                         {'label': 'Contact with heat', 'value': 'Contact with heat'},
                         {'label': 'Struck by powered moving object', 'value': 'Struck by powered moving object'},
                         {'label': 'Contact with electrical current', 'value': 'Contact with electrical current'},
                         {'label': 'Bodily reaction, NEC', 'value': 'Bodily reaction, NEC'},
                         {'label': 'Struck by rolling or sliding object',
                          'value': 'Struck by rolling or sliding object'},
                         {'label': 'Fall from scaffolds, walkways, platforms',
                          'value': 'Fall from scaffolds, walkways, platforms'},
                         {'label': 'NEC', 'value': 'NEC'},
                         {'label': 'Fall from ladders', 'value': 'Fall from ladders'},
                         {'label': 'Unclassified, insufficient data', 'value': 'Unclassified, insufficient data'},
                         {'label': 'Fall from piled material', 'value': 'Fall from piled material'},
                         {'label': 'Fall down stairs', 'value': 'Fall down stairs'},
                         {'label': 'Rubbed or abraded', 'value': 'Rubbed or abraded'},
                         {'label': 'Caught in, under or between two or more moving objects',
                          'value': 'Caught in, under or between two or more moving objects'},
                         {'label': 'Drowning', 'value': 'Drowning'},
                         {'label': 'Fall on save level, NEC', 'value': 'Fall on save level, NEC'},
                         {'label': 'Struck by concussion', 'value': 'Struck by concussion'},
                         {'label': 'Fall down raise, shaft or manway', 'value': 'Fall down raise, shaft or manway'},
                         {'label': 'Caught in, under or between collapsing material or buildings',
                          'value': 'Caught in, under or between collapsing material or buildings'},
                         {'label': 'Fall from headframe, derrick or tower',
                          'value': 'Fall from headframe, derrick or tower'},
                         {'label': 'Ingestion of radiations, caustics, toxic and noxious substances',
                          'value': 'Ingestion of radiations, caustics, toxic and noxious substances'},
                         {'label': 'Contact with cold', 'value': 'Contact with cold'},
                         {'label': 'Contact with cold objects or substances',
                          'value': 'Contact with cold objects or substances'},
                         {'label': 'No Value Found', 'value': 'No Value Found'},
                         {'label': '0', 'value': '0'},
                         {'label': '1', 'value': '1'}]
state_full_names = {
    'AL': 'Alabama', 'KY': 'Kentucky', 'TN': 'Tennessee', 'GA': 'Georgia', 'WV': 'West Virginia',
    'PA': 'Pennsylvania', 'IL': 'Illinois', 'AZ': 'Arizona', 'MT': 'Montana', 'CA': 'California',
    'NV': 'Nevada', 'TX': 'Texas', 'AR': 'Arkansas', 'MS': 'Mississippi', 'OK': 'Oklahoma',
    'ND': 'North Dakota', 'OR': 'Oregon', 'CO': 'Colorado', 'SD': 'South Dakota', 'NM': 'New Mexico',
    'WY': 'Wyoming', 'KS': 'Kansas', 'UT': 'Utah', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida',
    'ID': 'Idaho', 'WA': 'Washington', 'IN': 'Indiana', 'MI': 'Michigan', 'OH': 'Ohio', 'IA': 'Iowa',
    'MN': 'Minnesota', 'WI': 'Wisconsin', 'MO': 'Missouri', 'NE': 'Nebraska', 'VA': 'Virginia', 'LA': 'Louisiana',
    'ME': 'Maine', 'NH': 'New Hampshire', 'MD': 'Maryland', 'MA': 'Massachusetts', 'VT': 'Vermont', 'NJ': 'New Jersey',
    'NY': 'New York', 'NC': 'North Carolina', 'SC': 'South Carolina', 'RI': 'Rhode Island', 'AK': 'Alaska',
    'HI': 'Hawaii',
    'PR': 'Puerto Rico', 'VI': 'Virgin Islands', 'AS': 'American Samoa', 'GU': 'Guam', 'MP': 'Northern Mariana Islands'
}

states_options = [{'label': state_full_names[state_abbr], 'value': state_abbr} for state_abbr in states_options]


def create_figure(data_field, df, date_range, mining_types, values, coal_metal_ind):
    start_date, end_date = date_range
    years_between = [year for year in range(start_date, end_date + 1)]
    if (mining_types is None or mining_types == []) and (coal_metal_ind == None or coal_metal_ind == []):
        filter_condition = (df["CAL_YR"].between(start_date, end_date)) & df[data_field].isin(values)
        group_fields = ['CAL_YR', data_field]
        legend_title = data_field.replace("_", " ").title()
    elif (mining_types is None or mining_types == []) or (coal_metal_ind == None or coal_metal_ind == []):
        if (mining_types is None or mining_types == []):
            filter_condition = (df["CAL_YR"].between(start_date, end_date)) & df["COAL_METAL_IND"].isin(
                coal_metal_ind) & df[data_field].isin(values)
            group_fields = ['CAL_YR', 'COAL_METAL_IND', data_field]
            legend_title = data_field.replace("_", " ").title()
        elif (coal_metal_ind == None or coal_metal_ind == []):
            filter_condition = (df["CAL_YR"].between(start_date, end_date)) & df["SUBUNIT"].isin(mining_types) & df[
                data_field].isin(values)
            group_fields = ['CAL_YR', 'SUBUNIT', data_field]
            legend_title = data_field.replace("_", " ").title()
    else:
        filter_condition = (df["CAL_YR"].between(start_date, end_date)) & df["SUBUNIT"].isin(mining_types) & df[
            "COAL_METAL_IND"].isin(coal_metal_ind) & df[data_field].isin(values)
        group_fields = ['CAL_YR', 'SUBUNIT', 'COAL_METAL_IND', data_field]
        legend_title = data_field.replace("_", " ").title()

    data = df[filter_condition]
    dff = data[data['NO_INJURIES'] != 0].groupby(group_fields)['CAL_YR'].value_counts().reset_index(name='injuries')

    fig = go.Figure()
    fig.update_layout(
        title=dict(text="TOTAL NUMBER OF INJURIES", font=dict(size=18, family="sans-serif"), x=0.45),
        xaxis=dict(title_text="Years"),
        yaxis=dict(title_text="No of Injuries"),
        legend_title=legend_title,
        legend_title_font=dict(size=12),
        barmode="stack",
        showlegend=True,
        width=900, height=600
    )
    colors = px.colors.qualitative.Plotly
    for i, r in enumerate(dff[data_field].unique()):
        if mining_types is None or mining_types == []:
            plot_df = dff[dff[data_field] == r]
            fig.add_trace(
                go.Bar(x=plot_df.CAL_YR, y=plot_df.injuries,
                       name=r,
                       marker_color=colors[i % len(colors)],
                       hovertemplate='<b>Injuries:</b> %{y} <br>Year: %{x}<br>' + legend_title + ': ' + r + '<extra></extra>')
            )
            fig.update_xaxes(tickfont=dict(size=9, family='sans-serif'), type='category')
            fig.update_yaxes(tickfont=dict(size=9, family='sans-serif'))
            fig.update_layout(legend=dict(font=dict(size=7, family="sans-serif")))
        else:
            plot_df = dff[dff[data_field] == r]
            fig.add_trace(
                go.Bar(x=[plot_df.CAL_YR, plot_df.SUBUNIT], y=plot_df.injuries,
                       name=r,
                       marker_color=colors[i % len(colors)],
                       hovertemplate='<b>Injuries:</b> %{y} <br>Year: %{x}<br>' + legend_title + ': ' + r + '<extra></extra>')
            )
            fig.update_xaxes(tickfont=dict(size=9, family='sans-serif'))
            fig.update_yaxes(tickfont=dict(size=9, family='sans-serif'))
            fig.update_layout(legend=dict(font=dict(size=7, family="sans-serif")))

    return fig, data

modal = html.Div([
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Yearly Mine Statistics")),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    html.Div([
                        html.H4('Total Number of Injuries',
                                style={'textAlign': 'center', 'fontSize': 20}),
                        html.P(id='total_injuries_popup',
                               style={'textAlign': 'center', 'color': 'orange', 'fontSize': 20}),
                    ])
                ]),
                dbc.Col([
                    html.Br(),
                    html.Div([
                        html.H4('Total Number of Violations',
                                style={'textAlign': 'center', 'fontSize': 20}),
                        html.P(id='number_violations_popup',
                               style={'textAlign': 'center', 'color': '#e55467', 'fontSize': 20}),
                    ])
                ]),
                dbc.Col([
                    html.Br(),
                    html.Div([
                        html.H4('Total Amount of Penalty',
                                style={'textAlign': 'center', 'fontSize': 20}),
                        html.P(id='total_penalty_popup',
                               style={'textAlign': 'center', 'color': 'red', 'fontSize': 20}),
                    ])
                ]),
            ]),
            html.Div(id="popup-content"),
        ]),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-popup", value=False)
        ),
    ],
        id="popup-modal",
        size="xl",
    ),
])

app.layout = dbc.Container([
    dcc.Tabs(
        className="dbc", children=[
            dbc.Tab(
                label="Home", children=[
                    html.H1(id="General"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.Row([
                                    dbc.Col([
                                        dcc.Markdown("**Years**", style={'font-size': '12px'},
                                                     className="no-bottom-margin"),
                                        dcc.RangeSlider(
                                            id="date_slider_main",
                                            min=df["CAL_YR"].min(),
                                            max=df["CAL_YR"].max(),
                                            step=1,
                                            value=[df["CAL_YR"].min(), df["CAL_YR"].max()],
                                            marks=marks_year,
                                            vertical=True,
                                            className='custom-range-slider'
                                        )], width=3),
                                    dbc.Col([
                                        html.Label("Select State:", style={'font-size': '12px'}),
                                        dcc.Dropdown(
                                            id="states-dropdown",
                                            options=states_options,
                                            multi=True,
                                            placeholder="Select States (Default: All)",
                                            style={'font-size': '12px'}),
                                    ], width=8),
                                ]),
                                html.Button('Submit', id='submit-button_main', value=1)
                            ])
                        ], width=3),
                        dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                    html.Br(),
                                    html.Div([
                                        html.H4('Total Number of Injuries',
                                                style={'textAlign': 'center', 'color': 'black', 'fontSize': 20}),
                                        html.P(id='total_injuries_display',
                                               style={'textAlign': 'center', 'color': 'orange', 'fontSize': 20}),
                                    ], className='total_injuries')]),
                                dbc.Col([
                                    html.Br(),
                                    html.Div([
                                        html.H4('Total Number of Violations',
                                                style={'textAlign': 'center', 'color': 'black', 'fontSize': 20}),
                                        html.P(id='number_violations',
                                               style={'textAlign': 'center', 'color': '#e55467', 'fontSize': 20}),
                                    ], className='total_violations')]),
                                dbc.Col([
                                    html.Br(),
                                    html.Div([
                                        html.H4('Total Amount of Penalty',
                                                style={'textAlign': 'center', 'color': 'black', 'fontSize': 20}),
                                        html.P(id='total_penalty',
                                               style={'textAlign': 'center', 'color': 'red', 'fontSize': 20}),
                                    ], className='total_penalty')
                                ]),

                            ]),
                            dbc.Col([
                                html.Div([
                                    dcc.Graph(id="geographic-graph",
                                              figure=go.Figure(data=go.Scattergeo(locationmode='USA-states', ),
                                                               layout=dict(geo=dict(scope='usa',
                                                                                    projection=dict(type='albers usa'),
                                                                                    showland=True, showsubunits=True,
                                                                                    subunitcolor="darkblue")))),
                                    dcc.Store(id='yearly_df_store', data=None), ]),
                            ]),
                        ]),
                    ]), modal
                ]),
            dbc.Tab(label="Health and Safety Analysis", children=[
                html.H1(id="Dataset-title"),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            html.Div([
                                html.Label("Select Dataset:", style={'font-size': '12px'}),
                                dcc.Dropdown(
                                    id='dataset-dropdown',
                                    options=[
                                        {'label': 'Accidents', 'value': 'Accidents'},
                                        {'label': 'Violations', 'value': 'violations'},
                                    ],
                                    style={'width': '100%', 'font-size': '12px'}
                                ),
                            ], style={'padding': '10px'}),
                            html.Div([
                                html.Label("Select Variable", style={'font-size': '12px'}),
                                dcc.Dropdown(
                                    id="variable_type_dropdown",
                                    style={'font-size': '12px'}
                                ),
                            ], style={'padding': '10px'}),
                            html.Div(id="subunit_dropdown_container", style={'font-size': '12px', 'padding': '10px'}),
                            dbc.Row([
                                dbc.Col([
                                    dcc.Markdown("**Years**", style={'font-size': '12px'},
                                                 className="no-bottom-margin"),
                                    dcc.RangeSlider(
                                        id="date_slider",
                                        min=df["CAL_YR"].min(),
                                        max=df["CAL_YR"].max(),
                                        step=1,
                                        value=[df["CAL_YR"].min(), df["CAL_YR"].max()],
                                        marks=marks_year,
                                        vertical=True,
                                        className='custom-range-slider'
                                    ),
                                ], width=3),
                                html.Br(),
                                dbc.Col([
                                    dbc.Col([
                                        dcc.Markdown("**Mining Type**", className="no-bottom-margin",
                                                     style={'font-size': '12px'}),
                                        dcc.Checklist(
                                            id="mining_type_checklist",
                                            options=mining_type_options,
                                            labelStyle={'display': 'block', 'font-size': '10px'},
                                            className='custom-checklist'
                                        ),
                                    ], width=7),
                                    html.Br(),
                                    dbc.Col([
                                        dcc.Markdown("**Coal Metal Indicator**", className="no-bottom-margin",
                                                     style={'font-size': '12px'}),
                                        dcc.Checklist(
                                            id="coal_metal_checklist",
                                            options=coal_metal_options,
                                            labelStyle={'display': 'block', 'font-size': '10px'},
                                            className='custom-checklist'
                                        ),
                                    ], width=7)]),

                            ]),
                            html.Button('Submit', id='submit-button', value=1)
                        ])
                    ], width=3),
                    dbc.Col(dcc.Graph(id="injuries-graph"), width=9)
                ], justify="between"),
                html.Div(
                    style={'overflowX': 'auto'},
                    children=[
                        dash_table.DataTable(
                            id='data_table',
                            columns=[{"name": i, "id": i} for i in df.columns],
                            data=[],
                            style_table={'minWidth': '100%', 'height': '300px', 'overflowY': 'auto'},
                            filter_action='native',
                            sort_action='native',
                            export_format='csv',
                            style_header={
                                'backgroundColor': 'rgb(50, 50, 50)',
                                'color': 'lightgrey',
                                'font-family': 'Arial'
                            },
                            style_data={
                                'backgroundColor': 'rgb(80, 80, 80)',
                                'color': 'grey',
                                'font-family': 'Arial'
                            },
                            style_filter={
                                'backgroundColor': 'rgb(90, 90, 90)',
                                'color': 'grey',
                                'font-family': 'Arial'
                            }
                        )
                    ]
                )
            ]),
            dbc.Tab(label="AI-based Integrated Models", children=[html.H1(id="ai_models")], style={'display': 'flex'})
        ]),
], style={"width": 1500})


@app.callback(
    Output("geographic-graph", "figure"),
    Output('total_injuries_display', 'children'),
    Output('number_violations', 'children'),
    Output('total_penalty', 'children'),
    Output("submit-button_main", "n_clicks"),
    Output('yearly_df_store', 'data'),
    Input("date_slider_main", "value"),
    Input("submit-button_main", "n_clicks"),
    Input("states-dropdown", "value"),
)
def main_graph(date_range, n_clicks, states):
    if not n_clicks:
        fig = go.Figure(data=go.Scattergeo(locationmode='USA-states'),
                        layout=dict(geo=dict(scope='usa', projection=dict(type='albers usa'),
                                             showland=True, showsubunits=True, subunitcolor="darkblue", showframe=False,
                                             showcoastlines=False)))
        fig.update_layout(width=900, height=600)
        fig.update_layout(margin=dict(l=5, r=5, t=5, b=5))
        n_clicks = None
        t_injuries = 0
        t_violations = 0
        t_penalty = 0
        return fig, f"{t_injuries}", f"{t_violations}", f"{t_penalty}", n_clicks, None
    else:
        start_date, end_date = date_range
        years_between = [year for year in range(start_date, end_date + 1)]
        data = df[df["CAL_YR"].between(start_date, end_date)]
        injuries_df = data[data['NO_INJURIES'] != 0].groupby(['MINE_ID', 'CAL_YR'])[['MINE_ID', 'CAL_YR']].value_counts().reset_index(name='NO_INJURIES')
        viol_df = violations[violations["CAL_YR"].between(start_date, end_date)].groupby(['MINE_ID', 'CAL_YR'])[
            ['PROPOSED_PENALTY', 'AMOUNT_PAID', 'AMOUNT_DUE']].sum().reset_index()
        viol_df['NO_VIOLATIONS'] = \
        violations[violations["CAL_YR"].between(start_date, end_date)].groupby(['MINE_ID', 'CAL_YR'])[
            ['MINE_ID', 'CAL_YR']].value_counts().reset_index()['count']
        zero_inj_df = pd.DataFrame(
            data[~data.MINE_ID.isin(injuries_df.MINE_ID.unique())]['MINE_ID'].reset_index(drop=True))
        gr_data = pd.merge(injuries_df, zero_inj_df, on='MINE_ID', how='outer').fillna(0)
        merged_df = pd.merge(gr_data, viol_df, on=['MINE_ID', 'CAL_YR'], how='outer')
        if states == [] or states == None:
            sel_mines = mines[mines['MINE_ID'].isin(merged_df.MINE_ID.unique())].reset_index(drop=True)[
                ['MINE_ID', 'CURRENT_MINE_NAME', 'CURRENT_MINE_TYPE', 'CURRENT_MINE_STATUS', 'LONGITUDE', 'LATITUDE',
                 'STATE']]
        else:
            sel_mines = \
            mines[(mines['MINE_ID'].isin(merged_df.MINE_ID.unique())) & (mines['STATE'].isin(states))].reset_index(
                drop=True)[
                ['MINE_ID', 'CURRENT_MINE_NAME', 'CURRENT_MINE_TYPE', 'CURRENT_MINE_STATUS', 'LONGITUDE', 'LATITUDE',
                 'STATE']]
        yearly_df = pd.merge(merged_df, sel_mines, on='MINE_ID', how='inner')
        yearly_df_store = yearly_df.to_json(date_format='iso', orient='split')
        aggregations = {
            'NO_INJURIES': 'sum',
            'PROPOSED_PENALTY': 'sum',
            'AMOUNT_PAID': 'sum',
            'AMOUNT_DUE': 'sum',
            'NO_VIOLATIONS': 'sum',
            'CURRENT_MINE_NAME': 'first',
            'CURRENT_MINE_TYPE': 'first',
            'CURRENT_MINE_STATUS': 'first',
            'LONGITUDE': 'first',
            'LATITUDE': 'first',
            'STATE': 'first',
        }
        plot_data = yearly_df.groupby('MINE_ID').agg(aggregations).reset_index()

        t_injuries = "{:,}".format(int(np.ceil(plot_data.NO_INJURIES.sum())))
        t_violations = "{:,}".format(int(np.ceil(plot_data.NO_VIOLATIONS.sum())))
        t_penalty = "{:,}".format(int(np.ceil(plot_data.PROPOSED_PENALTY.sum())))

        fig = go.Figure(data=go.Scattergeo(
            locationmode='USA-states',
            lon=plot_data['LONGITUDE'],
            lat=plot_data['LATITUDE'],
            customdata=plot_data[
                ['MINE_ID', 'CURRENT_MINE_NAME', 'CURRENT_MINE_TYPE', 'CURRENT_MINE_STATUS', 'NO_INJURIES', 'STATE',
                 'NO_VIOLATIONS', 'PROPOSED_PENALTY', 'AMOUNT_PAID', 'AMOUNT_DUE']].astype(str),
            hovertemplate=(
                    'Mine ID: %{customdata[0]}<br>' +
                    'Mine Name: %{customdata[1]}' + ', ' + '%{customdata[5]}<br>' +
                    'Mine Type: %{customdata[2]}<br>' +
                    'Mine Status: %{customdata[3]}<br>' +
                    'Number of Injuries: %{customdata[4]}<br>' +
                    'Number of Violations: %{customdata[6]}<br>' +
                    'Total Proposed Penalty: %{customdata[7]}<br>' +
                    'Amount Paid: %{customdata[8]}<br>' +
                    'Amount Due: %{customdata[9]}'
            ),
            mode='markers',
            marker=dict(
                size=6,
                opacity=0.8,
                autocolorscale=False,
                symbol='circle',
                line=dict(
                    width=1,
                    color='rgba(102, 102, 102)'
                ),
                colorscale='YlOrRd',
                cmin=0,
                color=plot_data['NO_INJURIES'],
                cmax=plot_data['NO_INJURIES'].max(),
                colorbar=dict(title="Total Number of Injuries", len=0.7, x=1.22, xanchor='right', y=0.5,
                              yanchor='middle')
            )))
        fig.update_layout(title=dict(
            text='Total Number of Injuries at Each Mine Site',
            x=0.45,
            y=1,
            xanchor='center',
            yanchor='top',
            font=dict(
                size=20,
                color='Black',
            )),
            geo=dict(
                scope='usa',
                projection_type='albers usa',
                showland=True,
                showsubunits=True,
                subunitcolor="darkblue",
                showframe=False,
                showcoastlines=False,
                landcolor="rgb(250, 250, 250)",
                countrywidth=0.5,
                subunitwidth=0.5
            ),
            width=900,
            height=600)
        fig.update_layout(margin=dict(l=5, r=5, t=5, b=5))
        n_clicks = None
        return fig, f"{t_injuries}", f"{t_violations}", f"{t_penalty}", n_clicks, yearly_df_store


@app.callback(
    [
        Output("popup-modal", "is_open"),
        Output("popup-content", "children"),
        Output("geographic-graph", "clickData"),
        Output('total_injuries_popup', 'children'),
        Output('number_violations_popup', 'children'),
        Output('total_penalty_popup', 'children'),
        Output("close-popup", "n_clicks")
    ],
    [
        Input("geographic-graph", "clickData"),
        Input("close-popup", "n_clicks")
    ],
    [State("popup-modal", "is_open"),
     State("date_slider_main", "value"),
     State('yearly_df_store', 'data'),
     ],
)
def display_popup(click_data, n_clicks_pu, is_open, date_range, yearly_df_store):
    ctx = dash.callback_context
    triggered_id = ctx.triggered_id if ctx.triggered_id else ''
    if 'geographic-graph' in triggered_id:
        selected_mine_id = click_data['points'][0]['customdata'][0] if click_data else None
        start_date, end_date = date_range
        years_between = [year for year in range(start_date, end_date + 1)]
        yearly_df = pd.read_json(yearly_df_store, orient='split')
        click_fig_data = yearly_df[yearly_df['MINE_ID'] == int(selected_mine_id)]
        click_fig_data[['CAL_YR', 'NO_INJURIES', 'PROPOSED_PENALTY', 'AMOUNT_PAID',
                        'AMOUNT_DUE', 'NO_VIOLATIONS', 'LONGITUDE', 'LATITUDE']] = click_fig_data[
            ['CAL_YR', 'NO_INJURIES', 'PROPOSED_PENALTY', 'AMOUNT_PAID',
             'AMOUNT_DUE', 'NO_VIOLATIONS', 'LONGITUDE', 'LATITUDE']].apply(pd.to_numeric)
        t_injuries = "{:,}".format(int(np.ceil(click_fig_data.NO_INJURIES.sum())))
        t_violations = "{:,}".format(int(np.ceil(click_fig_data.NO_VIOLATIONS.sum())))
        t_penalty = "{:,}".format(int(np.ceil(click_fig_data.PROPOSED_PENALTY.sum())))

        fig = go.Figure()
        fig.add_trace(go.Bar(x=click_fig_data['CAL_YR'], y=click_fig_data['NO_INJURIES'], name='Injuries'))
        fig.add_trace(go.Bar(x=click_fig_data['CAL_YR'], y=click_fig_data['PROPOSED_PENALTY'], name='Proposed Penalty'))
        fig.add_trace(go.Bar(x=click_fig_data['CAL_YR'], y=click_fig_data['AMOUNT_PAID'], name='Amount Paid'))
        fig.add_trace(go.Bar(x=click_fig_data['CAL_YR'], y=click_fig_data['AMOUNT_DUE'], name='Amount Due'))
        fig.add_trace(
            go.Bar(x=click_fig_data['CAL_YR'], y=click_fig_data['NO_VIOLATIONS'], name='Number of Violations'))
        fig.update_layout(
            title=dict(text='Yearly Statistics', font=dict(size=18, family="sans-serif"), x=0.5),
            xaxis_title="Year",
            yaxis_title="Numbers",
            showlegend=True,
            barmode='group'
        )
        fig.update_xaxes(tickfont=dict(size=14, family='sans-serif'), type='category', tickvals=years_between)
        fig.update_yaxes(tickfont=dict(size=14, family='sans-serif'))

        popup_content = html.Div([
            html.H4(f"Mine ID: {selected_mine_id}", style={'fontSize': 13}),
            html.H4(f"Mine Name: {click_fig_data.CURRENT_MINE_NAME.iloc[0]}, {click_fig_data.STATE.iloc[0]}",
                    style={'fontSize': 13}),
            html.H4(f"Mine Type: {click_fig_data.CURRENT_MINE_TYPE.iloc[0]}", style={'fontSize': 13}),
            html.H4(f"Mine Status: {click_fig_data.CURRENT_MINE_STATUS.iloc[0]}", style={'fontSize': 13}),
            dcc.Graph(figure=fig)
        ])
        if n_clicks_pu:
            n_clicks_pu = None
            is_open = False
        else:
            is_open = True
        return is_open, popup_content, None, f'{t_injuries}', f'{t_violations}', f'{t_penalty}', n_clicks_pu
    else:
        return False, None, None, None, None, None, None


@app.callback(
    Output("variable_type_dropdown", "options"),
    Input('dataset-dropdown', "value")
)
def variable_options(dataset_ind):
    if dataset_ind is None or dataset_ind != 'Accidents':
        options = []
    else:
        options = [{'label': 'Total Injuries', 'value': 'total'},
                   {'label': 'Degree of Injury', 'value': 'DEGREE_INJURY'},
                   {'label': 'Injured Body Part', 'value': 'INJ_BODY_PART'},
                   {'label': 'Injury Source', 'value': 'INJURY_SOURCE'},
                   {'label': 'Nature of Injury', 'value': 'NATURE_INJURY'},
                   {'label': 'Classification', 'value': 'CLASSIFICATION'},
                   {'label': 'Accident Type', 'value': 'ACCIDENT_TYPE'}]
    return options


@app.callback(
    Output("subunit_dropdown_container", "children"),
    Input("variable_type_dropdown", "value"),
)
def data_type(data_type):
    if data_type is None:
        drop_down = dcc.Dropdown(id="dropdown",
                                 options=[])
    elif data_type == 'total':
        drop_down = dcc.Dropdown(id="dropdown",
                                 options=[])
    elif data_type == 'DEGREE_INJURY':
        drop_down = dcc.Dropdown(id="dropdown",
                                 options=degree_injury_options, multi=True)
    elif data_type == 'INJ_BODY_PART':
        drop_down = dcc.Dropdown(id="dropdown",
                                 options=injured_body_options, multi=True)
    elif data_type == 'INJURY_SOURCE':
        drop_down = dcc.Dropdown(id="dropdown",
                                 options=injury_source_options, multi=True)
    elif data_type == 'NATURE_INJURY':
        drop_down = dcc.Dropdown(id="dropdown",
                                 options=nature_injury_options, multi=True)
    elif data_type == 'CLASSIFICATION':
        drop_down = dcc.Dropdown(id="dropdown",
                                 options=classification_options, multi=True)
    elif data_type == 'ACCIDENT_TYPE':
        drop_down = dcc.Dropdown(id="dropdown",
                                 options=accident_type_options, multi=True)

    return drop_down


@app.callback(
    Output("injuries-graph", "figure"),
    Output("submit-button", "n_clicks"),
    Output('data_table', 'data'),
    Input('dataset-dropdown', 'value'),
    Input("variable_type_dropdown", "value"),
    Input("dropdown", "value"),
    Input("date_slider", "value"),
    Input("submit-button", "n_clicks"),
    Input("mining_type_checklist", "value"),
    Input("coal_metal_checklist", "value")
)
def update_graph(dataset_ind, data_type, sub_values, date_range, n_clicks, mining_types, coal_metal_ind):
    if dataset_ind is not None:
        file_path = f'{dataset_ind}.txt'
        df = pd.read_csv(file_path, delimiter='|', encoding='ISO-8859-1', low_memory=False)
    if data_type is None:
        fig = px.line()
        data = []
        return fig, n_clicks, data
    if data_type == 'total':
        if not n_clicks:
            fig = px.bar()
            data = []
            n_clicks = None
            return fig, n_clicks, data
        else:
            start_date, end_date = date_range
            years_between = [year for year in range(start_date, end_date + 1)]
            if (mining_types == None or mining_types == []) and (coal_metal_ind == None or coal_metal_ind == []):
                data = df[(df["CAL_YR"].between(start_date, end_date))]
                dff = data[data['NO_INJURIES'] != 0].groupby(['CAL_YR'])['CAL_YR'].value_counts().reset_index(
                    name='injuries')
                graph_title = f"TOTAL NUMBER OF INJURIES"
                fig = px.bar(dff, x="CAL_YR", y="injuries", barmode='group',
                             title=graph_title,
                             color_discrete_sequence=px.colors.qualitative.Plotly)
                fig.update_layout(
                    title=dict(font=dict(size=18, family="sans-serif"), x=0.5),
                    xaxis_title="Year",
                    yaxis_title="Number of Injuries",
                    width=900, height=600)
                fig.update_xaxes(tickfont=dict(size=12, family='sans-serif'), type='category', tickvals=years_between)
                fig.update_yaxes(tickfont=dict(size=12, family='sans-serif'))
                fig.update_traces(hovertemplate='<b>Injuries:</b> %{y}<br><b>Year:</b> %{x}<br><extra></extra>')
            elif (mining_types == None or mining_types == []) or (coal_metal_ind == None or coal_metal_ind == []):
                if (mining_types == None or mining_types == []):
                    data = df[
                        (df["CAL_YR"].between(start_date, end_date)) & (df["COAL_METAL_IND"].isin(coal_metal_ind))]
                    dff = data[data['NO_INJURIES'] != 0].groupby(['CAL_YR', 'COAL_METAL_IND'])[
                        'CAL_YR'].value_counts().reset_index(name='injuries')
                    graph_title = "TOTAL NUMBER OF INJURIES"
                    fig = px.bar(dff, x="CAL_YR", y="injuries", color="SUBUNIT", barmode='group',
                                 title=graph_title,
                                 color_discrete_sequence=px.colors.qualitative.Plotly)
                    fig.update_layout(
                        title=dict(font=dict(size=18, family="sans-serif"), x=0.5),
                        xaxis_title="Year",
                        yaxis_title="Number of Injuries",
                        legend_title="Coal or Metal Mining",
                        showlegend=True,
                        width=900, height=600)
                    fig.update_xaxes(tickfont=dict(size=12, family='sans-serif'), type='category',
                                     tickvals=years_between)
                    fig.update_yaxes(tickfont=dict(size=12, family='sans-serif'))
                    fig.for_each_trace(
                        lambda trace: trace.update(
                            customdata=dff[dff["COAL_METAL_IND"] == trace.name]["COAL_METAL_IND"],
                            hovertemplate='<b>Injuries:</b> %{y}<br><b>Year:</b> %{x}<br><b>Metal or Coal:</b> %{customdata}<extra></extra>'))
                elif (coal_metal_ind == None or coal_metal_ind == []):
                    data = df[(df["CAL_YR"].between(start_date, end_date)) & (df["SUBUNIT"].isin(mining_types))]
                    dff = data[data['NO_INJURIES'] != 0].groupby(['CAL_YR', 'SUBUNIT'])[
                        'CAL_YR'].value_counts().reset_index(name='injuries')
                    graph_title = f"TOTAL NUMBER OF INJURIES"
                    fig = px.bar(dff, x="CAL_YR", y="injuries", color="SUBUNIT", barmode='group',
                                 title=graph_title,
                                 color_discrete_sequence=px.colors.qualitative.Plotly)
                    fig.update_layout(
                        title=dict(font=dict(size=18, family="sans-serif"), x=0.5),
                        xaxis_title="Year",
                        yaxis_title="Number of Injuries",
                        legend_title="Mining Location",
                        showlegend=True,
                        width=900, height=500)
                    fig.update_xaxes(tickfont=dict(size=12, family='sans-serif'), type='category',
                                     tickvals=years_between)
                    fig.update_yaxes(tickfont=dict(size=12, family='sans-serif'))
                    fig.for_each_trace(
                        lambda trace: trace.update(
                            customdata=dff[dff["SUBUNIT"] == trace.name]["SUBUNIT"],
                            hovertemplate='<b>Injuries:</b> %{y}<br><b>Year:</b> %{x}<br><b>Mining Location:</b> %{customdata}<extra></extra>'))
            else:
                data = df[(df["CAL_YR"].between(start_date, end_date)) & (df["SUBUNIT"].isin(mining_types)) & (
                    df["COAL_METAL_IND"].isin(coal_metal_ind))]
                dff = data[data['NO_INJURIES'] != 0].groupby(['CAL_YR', 'SUBUNIT', 'COAL_METAL_IND'])[
                    'CAL_YR'].value_counts().reset_index(name='injuries')
                graph_title = f"TOTAL NUMBER OF INJURIES"
                fig = px.bar(dff, x="CAL_YR", y="injuries", color="SUBUNIT", barmode='group',
                             title=graph_title,
                             color_discrete_sequence=px.colors.qualitative.Plotly)
                fig.update_layout(
                    title=dict(font=dict(size=18, family="sans-serif"), x=0.5),
                    xaxis_title="Year",
                    yaxis_title="Number of Injuries",
                    legend_title="Mining Location",
                    showlegend=True,
                    width=900, height=600)
                fig.update_xaxes(tickfont=dict(size=12, family='sans-serif'), type='category', tickvals=years_between)
                fig.update_yaxes(tickfont=dict(size=12, family='sans-serif'))
                fig.for_each_trace(
                    lambda trace: trace.update(
                        hovertemplate='<b>Injuries:</b> %{y}<br><b>Year:</b> %{x}<br><extra></extra>'))
            n_clicks = None
            data = data.to_dict('records')
            return fig, n_clicks, data
    if data_type == 'DEGREE_INJURY':
        if not n_clicks or sub_values == None or sub_values == []:
            fig = px.bar()
            data = []
            n_clicks = None
            return fig, n_clicks, data
        else:
            fig, data = create_figure(data_type, df, date_range, mining_types, sub_values, coal_metal_ind)
            data = data.to_dict('records')
            n_clicks = None
            return fig, n_clicks, data
    if data_type == 'INJ_BODY_PART':
        if not n_clicks or sub_values == None or sub_values == []:
            fig = px.bar()
            data = []
            n_clicks = None
            return fig, n_clicks, data
        else:
            fig, data = create_figure(data_type, df, date_range, mining_types, sub_values, coal_metal_ind)
            data = data.to_dict('records')
            n_clicks = None
            return fig, n_clicks, data
    if data_type == 'INJURY_SOURCE':
        if not n_clicks or sub_values == None or sub_values == []:
            fig = px.bar()
            data = []
            n_clicks = None
            return fig, n_clicks, data
        else:
            fig, data = create_figure(data_type, df, date_range, mining_types, sub_values, coal_metal_ind)
            data = data.to_dict('records')
            n_clicks = None
            return fig, n_clicks, data
    if data_type == 'NATURE_INJURY':
        if sub_values == None or sub_values == [] or not n_clicks:
            fig = px.bar()
            data = []
            n_clicks = None
            return fig, n_clicks, data
        else:
            fig, data = create_figure(data_type, df, date_range, mining_types, sub_values, coal_metal_ind)
            data = data.to_dict('records')
            n_clicks = None
            return fig, n_clicks, data
    if data_type == 'CLASSIFICATION':
        if sub_values == None or sub_values == [] or not n_clicks:
            fig = px.bar()
            data = []
            n_clicks = None
            return fig, n_clicks, data
        else:
            fig, data = create_figure(data_type, df, date_range, mining_types, sub_values, coal_metal_ind)
            data = data.to_dict('records')
            n_clicks = None
            return fig, n_clicks, data
    if data_type == 'ACCIDENT_TYPE':
        if sub_values == None or sub_values == [] or not n_clicks:
            fig = px.bar()
            data = []
            n_clicks = None
            return fig, n_clicks, data
        else:
            fig, data = create_figure(data_type, df, date_range, mining_types, sub_values, coal_metal_ind)
            data = data.to_dict('records')
            n_clicks = None
            return fig, n_clicks, data

if __name__ == "__main__":
    app.run_server(debug = False)