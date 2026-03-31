#!/usr/bin/env python3
"""Generate contractor punch list PDFs for 13062 Callaway Ct pre-sale inspection."""

from fpdf import FPDF
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/mnt/c/Windows/Fonts"

PROPERTY = "13062 Callaway Ct, Fishers, IN 46037"
OWNER = "Onisuru Okotie"
DATE = "March 30, 2026"


class PunchListPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("TNR", "", os.path.join(FONT_DIR, "times.ttf"), uni=True)
        self.add_font("TNR", "B", os.path.join(FONT_DIR, "timesbd.ttf"), uni=True)
        self.add_font("TNR", "I", os.path.join(FONT_DIR, "timesi.ttf"), uni=True)
        self.add_font("TNR", "BI", os.path.join(FONT_DIR, "timesbi.ttf"), uni=True)
        self.set_auto_page_break(auto=True, margin=20)

    def header_block(self, title, subtitle=None):
        self.set_font("TNR", "B", 16)
        self.cell(0, 10, title, ln=True, align="C")
        self.ln(2)
        self.set_font("TNR", "", 12)
        self.cell(0, 6, f"Property: {PROPERTY}", ln=True, align="C")
        self.cell(0, 6, f"Owner: {OWNER}", ln=True, align="C")
        self.cell(0, 6, f"Inspection Date: {DATE}", ln=True, align="C")
        if subtitle:
            self.ln(2)
            self.set_font("TNR", "I", 11)
            self.multi_cell(0, 6, subtitle, align="C")
        self.ln(4)
        # Horizontal line
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def section_header(self, text):
        self.set_font("TNR", "B", 13)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 8, f"  {text}", ln=True, fill=True)
        self.ln(3)

    def item_row(self, ref, description, notes="", checkbox=True):
        x_start = self.get_x()
        y_start = self.get_y()

        # Check if we need a new page
        if y_start > 260:
            self.add_page()
            y_start = self.get_y()

        # Checkbox
        if checkbox:
            self.set_font("TNR", "", 12)
            self.cell(8, 6, "[ ]", ln=False)
        else:
            self.cell(8, 6, "", ln=False)

        # Reference number
        self.set_font("TNR", "B", 12)
        self.cell(14, 6, ref, ln=False)

        # Description
        self.set_font("TNR", "", 12)
        desc_width = 168 if not notes else 85
        self.cell(desc_width, 6, description, ln=False if notes else True)

        if notes:
            self.set_font("TNR", "I", 11)
            self.multi_cell(83, 6, notes)

        self.ln(2)

    def item_with_detail(self, ref, title, detail):
        y_start = self.get_y()
        if y_start > 255:
            self.add_page()

        # Checkbox + ref + title
        self.set_font("TNR", "", 12)
        self.cell(8, 7, "[ ]", ln=False)
        self.set_font("TNR", "B", 12)
        self.cell(14, 7, ref, ln=False)
        self.set_font("TNR", "B", 12)
        self.cell(0, 7, title, ln=True)

        # Detail indented
        self.set_x(32)
        self.set_font("TNR", "", 11)
        self.multi_cell(165, 6, detail)
        self.ln(3)

    def footer_note(self, text):
        self.ln(5)
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)
        self.set_font("TNR", "I", 10)
        self.multi_cell(0, 5, text)

    def signature_block(self):
        self.ln(10)
        self.set_font("TNR", "", 12)
        self.cell(90, 6, "Contractor Signature: _______________________", ln=False)
        self.cell(0, 6, "Date: _______________", ln=True)
        self.ln(6)
        self.cell(90, 6, "Homeowner Signature: _______________________", ln=False)
        self.cell(0, 6, "Date: _______________", ln=True)


def generate_plumber():
    pdf = PunchListPDF()
    pdf.add_page()
    pdf.header_block(
        "PLUMBER \u2014 Punch List",
        "Half-day visit. Gas leak repair is Priority #1.\nCall Citizens Gas first (317-924-3311) for free leak confirmation before scheduling."
    )

    pdf.section_header("GAS \u2014 URGENT / SAFETY")

    pdf.item_with_detail("5.7.1", "Gas Leak \u2014 Elevated Reading at Manifold",
        "Elevated combustible gas reading detected at gas manifold in basement. "
        "Citizens Gas should confirm and locate leak (free). Plumber to repair: "
        "tighten fittings, replace valve, or re-pipe connection as needed. "
        "Pressure test after repair. Provide written pressure test certificate.")

    pdf.item_with_detail("5.7.2", "Drip Leg / Sediment Trap Missing",
        "No drip leg/sediment trap on gas manifold. Current building code requires one. "
        "Install drip leg on gas manifold.")

    pdf.section_header("PLUMBING FIXTURES & FAUCETS")

    pdf.item_with_detail("5.2.1", "Toilet Loose at Base \u2014 Master Bathroom",
        "Toilet rocks at base. Replace wax ring, tighten closet bolts. "
        "Check flange condition \u2014 replace if corroded.")

    pdf.item_with_detail("5.2.2", "Fixtures Leaking + Aerator Replacement (6 sinks)",
        "Leaks noted at: Master bathroom (both sinks), 2nd floor southwest bathroom. "
        "Tighten connections, replace washers/cartridges as needed.\n\n"
        "Also: Replace aerators on all 6 bathroom sink faucets (homeowner-supplied). "
        "Faucets are calcified with poor spray patterns. CLR soak any calcified spouts.")

    pdf.item_with_detail("5.2.4", "Water Supply Line Leak",
        "Active leak at water supply connection. Repair or replace supply line. "
        "This is an active leak \u2014 priority item.")

    pdf.item_with_detail("5.3.1", "Drain Leak \u2014 Master Bath East Sink",
        "Leak at P-trap / drain connection under master bathroom east sink. "
        "Tighten or replace drain assembly.")

    pdf.item_with_detail("5.3.4", "Vent Pipe \u2014 Drain Pipe (Sewage Ejector)",
        "Both pipes from sewage ejector connected to sewer pipe. One should be "
        "connected to venting system. Evaluate and correct if needed. "
        "Improper venting can cause sewer gas intrusion.")

    pdf.section_header("APPLIANCES")

    pdf.item_with_detail("6.1.1", "Dishwasher High Loop Missing",
        "Dishwasher drain hose missing high loop. Install high loop to prevent "
        "backflow into dishwasher.")

    pdf.item_with_detail("6.1.3", "Dishwasher Leak",
        "Dishwasher leaked during cycle. Diagnose cause: connection, door gasket, "
        "or pump failure. Repair as needed.")

    pdf.item_with_detail("6.4.1", "Garbage Disposal Motor Locked",
        "Insinkerator disposal motor locked up. Try Allen key reset first. "
        "If motor is burnt, replace unit.")

    pdf.section_header("EXTERIOR FAUCETS")

    pdf.item_with_detail("3.8.1", "Exterior Faucet Leaking \u2014 East Side",
        "Hose bib leaking while running. Replace washer or replace hose bib.")

    pdf.item_with_detail("3.8.2", "Exterior Faucet Not Secure \u2014 East Side",
        "Faucet loose from wall. Re-secure with mounting bracket to prevent "
        "supply pipe damage.")

    pdf.footer_note(
        "Please provide itemized invoice with descriptions of all work completed. "
        "Include gas pressure test certificate. All work must be performed by a licensed plumber. "
        "Receipts and documentation will be provided to buyers as part of seller disclosure."
    )
    pdf.signature_block()

    pdf.output(os.path.join(OUTPUT_DIR, "01_Plumber_Punch_List.pdf"))
    print("Generated: 01_Plumber_Punch_List.pdf")


def generate_electrician():
    pdf = PunchListPDF()
    pdf.add_page()
    pdf.header_block(
        "ELECTRICIAN \u2014 Punch List",
        "Estimated 1\u20132 hour visit."
    )

    pdf.section_header("SAFETY ITEMS")

    pdf.item_with_detail("7.6.1", "Reverse Polarity \u2014 East Bedroom",
        "One or more receptacles wired with reversed polarity (hot/neutral swapped). "
        "Shock hazard. Swap wires to correct polarity. Test all outlets in room "
        "to confirm no others are affected.")

    pdf.section_header("FIXTURES & RECEPTACLES")

    pdf.item_with_detail("7.4.2", "Loose Receptacle \u2014 Loft",
        "Outlet pulling from wall. Tighten outlet box screws and ensure "
        "secure mounting.")

    pdf.item_with_detail("7.4.1", "Inoperable Lights \u2014 Multiple Locations",
        "Lights not operating in the following locations:\n"
        "\u2022 Garage\n"
        "\u2022 Master bedroom closet\n"
        "\u2022 Laundry room\n"
        "\u2022 2nd floor west bathroom\n"
        "\u2022 East bathroom\n\n"
        "May be burnt bulbs \u2014 test with new bulbs first. If new bulbs don't work, "
        "diagnose wiring/switch issue and repair.")

    pdf.footer_note(
        "Please provide itemized invoice with descriptions of all work completed. "
        "All work must be performed by a licensed electrician. "
        "Receipts will be provided to buyers as part of seller disclosure."
    )
    pdf.signature_block()

    pdf.output(os.path.join(OUTPUT_DIR, "02_Electrician_Punch_List.pdf"))
    print("Generated: 02_Electrician_Punch_List.pdf")


def generate_handyman():
    pdf = PunchListPDF()
    pdf.add_page()
    pdf.header_block(
        "HANDYMAN \u2014 Punch List",
        "Full-day visit. Pre-ordered parts noted with *.\n"
        "Order Pella parts, smoke/CO detectors, and egress ladder in advance."
    )

    pdf.section_header("SAFETY \u2014 PRIORITY")

    pdf.item_with_detail("7.8.1", "* Replace ALL Smoke Detectors",
        "All smoke detectors are past 10-year design life. Replace every unit "
        "in the house with new interconnected smoke detectors. Locations: "
        "every floor including basement, every bedroom, hallways outside sleeping areas.")

    pdf.item_with_detail("7.9.1", "* Install CO Detectors \u2014 Every Floor",
        "Inadequate CO detectors for a home with gas appliances. "
        "Install one CO detector on each floor (minimum 3\u20134 units).")

    pdf.item_with_detail("10.9.3", "Garage Auto-Reverse Sensor Not Working",
        "Auto pressure reverse sensor not responding. Federal CPSC safety requirement. "
        "Check photo-eye sensor alignment first (free fix). If sensors are dead, "
        "replace sensors or opener. Test both contact reverse and photo-eye after repair.")

    pdf.section_header("GARAGE & EXTERIOR DOORS")

    pdf.item_with_detail("10.9.1", "Garage Pedestrian Door Seal",
        "Door into house does not seal well \u2014 allows garage gases into living space. "
        "Install new weatherstripping around full perimeter.")

    pdf.item_with_detail("10.9.2", "Garage Door Weatherstripping \u2014 Middle Door",
        "Bottom seal damaged/deteriorated. Replace bottom weatherstrip seal.")

    pdf.item_with_detail("3.3.1", "Front Entry Door \u2014 Daylight Visible",
        "Light visible around front door frame. Adjust door and/or install "
        "new weatherstripping to eliminate gaps.")

    pdf.item_with_detail("3.3.2", "Exterior Door Seal \u2014 South",
        "Door does not sit tight against weatherstripping. "
        "Replace weatherstripping or adjust door.")

    pdf.item_with_detail("3.3.3", "Sliding Screen Door \u2014 Latch Missing",
        "Install replacement latch on sliding screen door.")

    pdf.section_header("EXTERIOR")

    pdf.item_with_detail("3.2.6", "Shutter Damaged",
        "Replace damaged decorative shutter. Match existing style and color.")

    pdf.item_with_detail("3.2.2", "Loose Siding \u2014 East Side",
        "Fiber cement siding pulling away. Re-nail securely and caulk seams.")

    pdf.item_with_detail("3.8.4", "* Egress Well Steps \u2014 East Side",
        "Egress window well has no ladder/steps. Code requirement for basement "
        "bedrooms. Install egress well ladder.")

    pdf.item_with_detail("3.5.1", "Walkway Trip Hazard \u2014 NE and South",
        "Concrete walkway has settled creating a lip/trip hazard. "
        "Grind down the lip or arrange for mudjacking.")

    pdf.item_with_detail("3.6.1", "Soffit Damage \u2014 Northwest",
        "Damaged soffit panel. Replace to prevent pest and water entry.")

    pdf.item_with_detail("4.4.1", "Clean All Gutters",
        "Debris accumulated in gutters. Clean all gutters around the house "
        "to restore proper water flow.")

    pdf.section_header("INTERIOR DOORS (7 locations)")

    pdf.item_with_detail("10.7.1", "Doors Don\u2019t Latch (x7)",
        "Adjust strike plates and/or latch hardware at:\n"
        "\u2022 Basement bedroom\n"
        "\u2022 Basement (other)\n"
        "\u2022 Master bedroom closet\n"
        "\u2022 Laundry room\n"
        "\u2022 Pocket door\n"
        "\u2022 Northwest bedroom closet\n"
        "\u2022 2nd floor west bathroom")

    pdf.item_with_detail("10.7.2", "Door Sticks \u2014 2nd Floor SW Bedroom",
        "Sand or plane the edge of the door to allow smooth operation.")

    pdf.item_with_detail("10.7.3", "Ball Latch Not Working",
        "Replace non-functional ball latch.")

    pdf.item_with_detail("10.7.4", "Ball Latch Missing \u2014 2nd Floor Loft",
        "Install new ball latch on loft door.")

    pdf.section_header("PLUMBING \u2014 MINOR")

    pdf.item_with_detail("5.2.3", "Bathtub Stopper Missing \u2014 2nd Floor West Bath",
        "Install universal bathtub drain stopper.")

    pdf.item_with_detail("5.2.5", "Fixture Loose \u2014 Laundry Room",
        "Tighten faucet mounting hardware.")

    pdf.item_with_detail("5.3.2", "Sink Stopper Not Connected (x2)",
        "Reconnect pop-up stopper pivot rod under sink at:\n"
        "\u2022 Northwest bathroom sink\n"
        "\u2022 2nd floor southwest bathroom")

    pdf.section_header("APPLIANCES & MISC")

    pdf.item_with_detail("6.1.2", "Dishwasher Not Secured \u2014 Basement",
        "Bracket dishwasher to countertop or cabinet with mounting screws.")

    pdf.item_with_detail("10.3.3", "Ceiling Cosmetic Damage \u2014 Loft",
        "Spackle and paint ceiling damage in loft area.")

    pdf.item_with_detail("10.6.1", "Drawer Off Track \u2014 2nd Floor East Bath",
        "Re-align drawer slides.")

    pdf.item_with_detail("10.6.3", "Missing Cabinet Hardware \u2014 Laundry Room",
        "Install matching knobs/pulls on cabinets.")

    pdf.section_header("WINDOWS \u2014 PELLA PARTS (* pre-ordered)")

    pdf.item_with_detail("10.8.8", "* Window Mechanism Covers (x2)",
        "Replace damaged protective covers over crank mechanisms at:\n"
        "\u2022 Master bathroom\n"
        "\u2022 Loft")

    pdf.item_with_detail("10.8.5", "* Window Missing Hardware (x3)",
        "Install replacement window hardware at:\n"
        "\u2022 Basement bedroom\n"
        "\u2022 East bedroom\n"
        "\u2022 Loft")

    pdf.item_with_detail("TRY", "Casement Windows \u2014 Try Silicone Spray",
        "Several casement windows won\u2019t close fully. Before calling Pella:\n"
        "1. Apply silicone spray to weatherstripping on all non-closing casements\n"
        "2. Lubricate hinges with silicone spray\n"
        "3. Clean any debris from hinge channels\n\n"
        "Locations: 1st floor SW, Master bedroom, NW bedroom, Formal dining room\n\n"
        "If this fixes them, great. If not, owner will call Pella service.")

    pdf.footer_note(
        "Please provide itemized invoice with descriptions of all work completed. "
        "* items require pre-ordered parts \u2014 confirm with homeowner before visit. "
        "Receipts will be provided to buyers as part of seller disclosure."
    )
    pdf.signature_block()

    pdf.output(os.path.join(OUTPUT_DIR, "03_Handyman_Punch_List.pdf"))
    print("Generated: 03_Handyman_Punch_List.pdf")


def generate_mason():
    pdf = PunchListPDF()
    pdf.add_page()
    pdf.header_block(
        "MASON \u2014 Punch List",
        "Schedule AFTER structural engineer assessment of chimney separation.\n"
        "Repairs should follow engineer\u2019s specifications."
    )

    pdf.section_header("CHIMNEY \u2014 STRUCTURAL (per engineer report)")

    pdf.item_with_detail("4.5.4", "Chimney Separation from House",
        "Visible gap between chimney and house siding. Structural engineer will "
        "determine if this is active settling or stable/cosmetic. "
        "Repair per engineer\u2019s specification \u2014 may require helical piers "
        "if active, or tuckpointing/caulk if stable. Provide written documentation "
        "of repair method and warranty.")

    pdf.section_header("CHIMNEY \u2014 WATER INTRUSION & MASONRY")

    pdf.item_with_detail("4.5.1", "Chimney Water Staining (Black Discoloration)",
        "Significant black water staining running down chimney stone. Indicates "
        "uncontrolled water runoff \u2014 likely from deteriorated crown, missing cap, "
        "or failed flashing at roofline. Address the water source (cap/crown/flashing), "
        "then clean exterior stone with masonry-appropriate cleaner. "
        "Apply waterproofing sealant after cleaning.")

    pdf.item_with_detail("4.5.2", "Chimney Cracked",
        "Visible cracking in chimney mortar/stone joints. "
        "Repoint all cracked mortar joints. Replace any damaged stones.")

    pdf.item_with_detail("4.5.3", "Chimney Loose Stone",
        "Stone on chimney is loose. Risk of water penetration. "
        "Re-set loose stones with proper mortar.")

    pdf.section_header("EXTERIOR STONE VENEER")

    pdf.item_with_detail("3.2.5", "Loose Stone \u2014 Southwest Exterior Wall",
        "Stone veneer piece separating near window on southwest side. "
        "Repoint and re-set stone to prevent water and pest intrusion.")

    pdf.footer_note(
        "Please provide:\n"
        "\u2022 Itemized invoice with descriptions of all work\n"
        "\u2022 Written assessment of chimney condition after repair\n"
        "\u2022 Warranty information for all masonry work\n"
        "\u2022 Before/after photos if possible\n\n"
        "All documentation will be provided to buyers as part of seller disclosure."
    )
    pdf.signature_block()

    pdf.output(os.path.join(OUTPUT_DIR, "04_Mason_Punch_List.pdf"))
    print("Generated: 04_Mason_Punch_List.pdf")


def generate_siding_painter():
    pdf = PunchListPDF()
    pdf.add_page()
    pdf.header_block(
        "SIDING & PAINT CONTRACTOR \u2014 Punch List",
        "Exterior trim repair and paint touch-up."
    )

    pdf.section_header("WOOD ROT \u2014 TRIM REPLACEMENT")

    pdf.item_with_detail("3.2.1", "Wood Rot on Exterior Trim \u2014 Multiple Elevations",
        "Wood rot noted on trim around the house. Affected areas identified "
        "on southeast, east, northeast, and northwest elevations. "
        "Evaluate and replace all affected trim boards. Address source of "
        "water intrusion where possible.")

    pdf.item_with_detail("10.8.3", "Window Wood Rot \u2014 South and Southwest",
        "Wood rot on exterior window trim. South and southwest sides. "
        "Replace affected trim material and seal properly.")

    pdf.section_header("PAINT")

    pdf.item_with_detail("3.2.4", "Paint Needed \u2014 Siding/Trim",
        "Areas of siding and trim are worn and need maintenance paint. "
        "After all rot repairs are complete, paint/touch-up all repaired areas "
        "and any other visibly worn trim to match existing color scheme.")

    pdf.footer_note(
        "Please provide itemized invoice with descriptions of all work completed. "
        "Include warranty information for rot repairs. "
        "Receipts will be provided to buyers as part of seller disclosure."
    )
    pdf.signature_block()

    pdf.output(os.path.join(OUTPUT_DIR, "05_Siding_Paint_Punch_List.pdf"))
    print("Generated: 05_Siding_Paint_Punch_List.pdf")


def generate_glass():
    pdf = PunchListPDF()
    pdf.add_page()
    pdf.header_block(
        "GLASS COMPANY \u2014 Punch List",
        "Sliding patio door \u2014 glass panel replacement."
    )

    pdf.section_header("FAILED THERMAL SEAL")

    pdf.item_with_detail("3.3.4", "Patio Door \u2014 Clouded/Foggy Glass (Failed Seal)",
        "Main rear sliding patio door has a failed thermal seal between the "
        "double-pane insulated glass unit (IGU). Moisture has entered between "
        "panes causing permanent fog/cloudiness.\n\n"
        "Requesting: Glass-only IGU panel replacement (not full door replacement). "
        "Door frame and track are in good condition.\n\n"
        "Location: Main living area, south-facing sliding patio door.")

    pdf.footer_note(
        "Please provide itemized invoice. Glass-only replacement preferred if "
        "frame/track are sound. Full door replacement quote also welcome for comparison. "
        "Receipt will be provided to buyers as part of seller disclosure."
    )
    pdf.signature_block()

    pdf.output(os.path.join(OUTPUT_DIR, "06_Glass_Company_Punch_List.pdf"))
    print("Generated: 06_Glass_Company_Punch_List.pdf")


def generate_calling_cheatsheet():
    pdf = PunchListPDF()
    pdf.add_page()
    pdf.header_block(
        "CONTRACTOR CALL CHEAT SHEET",
        "Use this when calling to schedule each contractor.\n"
        "Property: 13062 Callaway Ct, Fishers, IN 46037"
    )

    # Citizens Gas
    pdf.section_header("1. CITIZENS GAS \u2014 Call Monday (Free)")
    pdf.set_font("TNR", "", 12)
    pdf.cell(0, 7, "Phone: 317-924-3311", ln=True)
    pdf.ln(2)
    pdf.set_font("TNR", "I", 11)
    pdf.multi_cell(0, 6,
        "\"Hi, I had a home inspection today and the inspector detected an elevated "
        "gas reading near my gas manifold in the basement. I'd like to schedule "
        "a free leak detection visit. The address is 13062 Callaway Ct, Fishers 46037.\"")
    pdf.ln(4)

    # Structural Engineer
    pdf.section_header("2. STRUCTURAL ENGINEER \u2014 Call Monday")
    pdf.set_font("TNR", "", 12)
    pdf.cell(0, 7, "Contractor: ______________________________  Phone: ____________________", ln=True)
    pdf.ln(2)
    pdf.set_font("TNR", "I", 11)
    pdf.multi_cell(0, 6,
        "\"I'm preparing to list my home and had a pre-sale inspection. The inspector "
        "found chimney separation from the house \u2014 a visible gap between the chimney "
        "and siding. I need a structural assessment to determine if it's active settling "
        "or cosmetic, and a written report I can provide to buyers. It's a stone chimney "
        "on a 2-story home. When can you come out, and what's your fee for an assessment?\"")
    pdf.ln(4)

    # Plumber
    pdf.section_header("3. PLUMBER \u2014 Schedule After Gas Utility Visit")
    pdf.set_font("TNR", "", 12)
    pdf.cell(0, 7, "Contractor: ______________________________  Phone: ____________________", ln=True)
    pdf.ln(2)
    pdf.set_font("TNR", "I", 11)
    pdf.multi_cell(0, 6,
        "\"I'm listing my home and had a pre-sale inspection with 12 plumbing items. "
        "The biggest is a gas leak at the manifold \u2014 Citizens Gas has confirmed it. "
        "I also need a missing drip leg installed, a loose toilet re-set, several "
        "fixture leaks fixed, a supply line leak repaired, a dishwasher high loop added, "
        "a dishwasher leak diagnosed, a garbage disposal that's locked up, and two exterior "
        "faucets fixed. I'm thinking a half-day visit. Can you give me a ballpark and "
        "when you're available? I'll email you the full punch list.\"")
    pdf.ln(4)

    # Electrician
    pdf.section_header("4. ELECTRICIAN \u2014 1\u20132 Hour Visit")
    pdf.set_font("TNR", "", 12)
    pdf.cell(0, 7, "Contractor: ______________________________  Phone: ____________________", ln=True)
    pdf.ln(2)
    pdf.set_font("TNR", "I", 11)
    pdf.multi_cell(0, 6,
        "\"I need a quick visit \u2014 a reverse polarity outlet in a bedroom, a loose "
        "receptacle in the loft, and 5 lights that aren't working across the house "
        "(might just be bulbs, might be wiring). Should be 1\u20132 hours. "
        "What's your service call rate?\"")
    pdf.ln(4)

    # Handyman
    pdf.section_header("5. HANDYMAN \u2014 Full Day")
    pdf.set_font("TNR", "", 12)
    pdf.cell(0, 7, "Contractor: ______________________________  Phone: ____________________", ln=True)
    pdf.ln(2)
    pdf.set_font("TNR", "I", 11)
    pdf.multi_cell(0, 6,
        "\"I'm getting my house ready to list and have about 30 small items from "
        "the inspection. Smoke and CO detector replacement throughout the house, "
        "garage door sensor repair, weatherstripping on several doors, 7 interior doors "
        "that don't latch, window hardware installation, gutter cleaning, an egress "
        "ladder install, a walkway trip hazard, soffit repair, and several other small "
        "items. I'm thinking a full day. What's your day rate? I'll email the full "
        "punch list. I'll pre-order all the parts.\"")
    pdf.ln(4)

    # Mason
    pdf.add_page()
    pdf.section_header("6. MASON \u2014 After Engineer Report")
    pdf.set_font("TNR", "", 12)
    pdf.cell(0, 7, "Contractor: ______________________________  Phone: ____________________", ln=True)
    pdf.ln(2)
    pdf.set_font("TNR", "I", 11)
    pdf.multi_cell(0, 6,
        "\"I have a stone chimney that's separating from the house, with cracked mortar, "
        "loose stones, and water staining. I'm getting a structural engineer report first "
        "and will have that before you come out. I also have loose stone veneer on the "
        "southwest exterior wall. Looking for someone to do all the masonry repairs, "
        "clean the chimney exterior, and apply waterproofing. Can I send you photos "
        "and the punch list?\"")
    pdf.ln(4)

    # Siding/Paint
    pdf.section_header("7. SIDING / TRIM / PAINT CONTRACTOR")
    pdf.set_font("TNR", "", 12)
    pdf.cell(0, 7, "Contractor: ______________________________  Phone: ____________________", ln=True)
    pdf.ln(2)
    pdf.set_font("TNR", "I", 11)
    pdf.multi_cell(0, 6,
        "\"I have wood rot on exterior trim in several spots \u2014 southeast, east, "
        "northeast, northwest sides, plus window trim on the south and southwest. "
        "Need the rotted trim replaced and everything painted to match. "
        "It's a stone and fiber cement/wood siding home. Can you come take a look "
        "and give me a quote?\"")
    pdf.ln(4)

    # Glass Company
    pdf.section_header("8. GLASS COMPANY \u2014 Patio Door")
    pdf.set_font("TNR", "", 12)
    pdf.cell(0, 7, "Contractor: ______________________________  Phone: ____________________", ln=True)
    pdf.ln(2)
    pdf.set_font("TNR", "I", 11)
    pdf.multi_cell(0, 6,
        "\"I have a sliding patio door with a failed thermal seal \u2014 the glass is "
        "foggy/clouded between the panes. The frame and track work fine, so I'm "
        "hoping for a glass-only IGU replacement rather than a full door swap. "
        "Can you give me a quote? It's the main rear patio door, south-facing.\"")
    pdf.ln(4)

    # Quotes Only
    pdf.section_header("9. ROOFER \u2014 Quote Only (Don't Fix)")
    pdf.set_font("TNR", "", 12)
    pdf.cell(0, 7, "Contractor: ______________________________  Phone: ____________________", ln=True)
    pdf.ln(2)
    pdf.set_font("TNR", "I", 11)
    pdf.multi_cell(0, 6,
        "\"I'm listing my home and the roof is 20\u201322 years old on fiberglass/asphalt "
        "shingles. I'm not planning to replace it before selling, but I need a written "
        "estimate for full replacement so I can provide it to buyers. It's a large home "
        "\u2014 about 6,100 square feet, gable roof. Can you come out and give me a "
        "written quote?\"")
    pdf.ln(4)

    pdf.section_header("10. PELLA SERVICE \u2014 Quote Only (If Handyman Fix Fails)")
    pdf.set_font("TNR", "", 12)
    pdf.cell(0, 7, "Phone: 888-847-3552 (Pella service)", ln=True)
    pdf.ln(2)
    pdf.set_font("TNR", "I", 11)
    pdf.multi_cell(0, 6,
        "\"I have 4 Pella casement windows that crank fine but won't fully close/seal. "
        "The cranks work \u2014 it seems like a weatherstripping or hinge issue. "
        "Locations: 1st floor southwest, master bedroom, northwest bedroom, and "
        "formal dining room. I need a service quote for repair. I'm preparing to list "
        "the home.\"")
    pdf.ln(4)

    pdf.section_header("11. HVAC \u2014 Tune-Up + Furnace Eval (Quote Only)")
    pdf.set_font("TNR", "", 12)
    pdf.cell(0, 7, "Contractor: ______________________________  Phone: ____________________", ln=True)
    pdf.ln(2)
    pdf.set_font("TNR", "I", 11)
    pdf.multi_cell(0, 6,
        "\"I'd like to schedule an HVAC tune-up. The furnace is a 10-year-old Carrier "
        "and the inspector noted some corrosion. I need an evaluation of whether it's "
        "surface corrosion or something more serious, plus a written assessment I can "
        "share with buyers. Two AC units \u2014 8 and 10 years old, Carrier, both working fine.\"")

    pdf.footer_note(
        "SEQUENCING REMINDER:\n"
        "1. Citizens Gas + Structural Engineer \u2014 this week\n"
        "2. Plumber + Electrician \u2014 after gas utility confirms leak\n"
        "3. Mason \u2014 after engineer report\n"
        "4. Siding/Paint + Glass Company \u2014 anytime\n"
        "5. Handyman \u2014 after Pella parts arrive (order now)\n"
        "6. Roofer + Pella + HVAC \u2014 quotes only, anytime"
    )

    # --- PRE-ORDER / SHOPPING LIST ---
    pdf.add_page()
    pdf.section_header("PRE-ORDER SHOPPING LIST")
    pdf.set_font("TNR", "I", 11)
    pdf.multi_cell(0, 6,
        "Order these items NOW so they arrive before the handyman visit. "
        "Have everything on-site and ready to install.")
    pdf.ln(4)

    shopping_items = [
        ("Smoke Detectors", "Interconnected, 10-year sealed battery. Need enough for every "
         "bedroom, every hallway outside sleeping areas, every floor including basement. "
         "Estimate 10-12 units for a home this size. Buy a combo pack if available.\n"
         "Example: Kidde or First Alert 10-year sealed, wireless interconnect."),
        ("CO Detectors", "One per floor (basement, 1st floor, 2nd floor, loft). "
         "Minimum 3-4 units. Can be combo smoke/CO units to reduce total count.\n"
         "Example: Kidde or First Alert plug-in with battery backup."),
        ("Egress Window Well Ladder", "One ladder for east-side basement egress well. "
         "Measure the well depth before ordering.\n"
         "Example: Bilco or Werner egress well ladder (Home Depot / Lowe's)."),
        ("Weatherstripping Assortment", "For front entry door, exterior door (south), "
         "garage pedestrian door. Get a variety pack or measure each door.\n"
         "Include: adhesive foam tape, door sweep, V-strip as needed."),
        ("Garage Door Bottom Seal", "Replacement rubber bottom seal for middle garage door. "
         "Measure width of door before ordering."),
        ("Sliding Screen Door Latch", "Replacement latch/pull for sliding screen door. "
         "Check style (hook latch vs lever) before ordering."),
        ("Replacement Shutter", "One decorative shutter to match existing. "
         "Measure height and width. Match color and style."),
        ("Bathtub Drain Stopper", "Universal bathtub stopper for 2nd floor west bathroom. "
         "Measure drain size (typically 1.5\")."),
        ("Cabinet Knobs/Pulls", "Matching hardware for laundry room cabinets. "
         "Bring an existing knob to the store to match, or measure hole spacing."),
        ("Pella Window Hardware (x3)", "Replacement window hardware for basement bedroom, "
         "east bedroom, and loft windows. Call Pella (888-847-3552) or check pella.com/shop "
         "with your window model number to order correct parts."),
        ("Pella Crank Mechanism Covers (x2)", "Replacement protective covers for master "
         "bathroom and loft windows. Same as above \u2014 need model number."),
        ("Faucet Aerators (x6)", "Replacement aerators for all 6 bathroom sink faucets. "
         "Remove one existing aerator and bring it to the store to match thread size "
         "(most are standard 15/16\" male or 55/64\" female). Buy 6."),
        ("CLR Calcium Remover", "One bottle of CLR or Lime-A-Way for soaking calcified "
         "faucet spouts. Plumber/handyman applies during visit."),
        ("Silicone Spray Lubricant", "For handyman to try on casement window weatherstripping "
         "and hinges. One can of silicone spray (e.g., WD-40 Specialist Silicone).\n"
         "NOT regular WD-40 \u2014 must be silicone-based."),
        ("Light Bulbs", "Assorted bulbs for 5 locations: garage, master closet, laundry room, "
         "2nd floor west bath, east bath. Check fixture types before buying.\n"
         "Bring old bulbs if possible to match."),
        ("Spackle + Paint (Loft Ceiling)", "Small tub of lightweight spackle + matching "
         "ceiling paint for loft ceiling cosmetic repair. Check existing ceiling color."),
        ("Door Strike Plates / Latch Hardware", "May need replacement strike plates or "
         "latch assemblies for up to 7 doors. Buy a multi-pack of adjustable strike "
         "plates. Handyman may also need wood filler + chisel for strike plate adjustment."),
    ]

    for name, detail in shopping_items:
        y = pdf.get_y()
        if y > 250:
            pdf.add_page()
        pdf.set_font("TNR", "", 12)
        pdf.cell(8, 7, "[ ]", ln=False)
        pdf.set_font("TNR", "B", 12)
        pdf.cell(0, 7, name, ln=True)
        pdf.set_x(18)
        pdf.set_font("TNR", "", 11)
        pdf.multi_cell(179, 5.5, detail)
        pdf.ln(3)

    # Estimated costs
    pdf.ln(4)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.3)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)
    pdf.set_font("TNR", "B", 12)
    pdf.cell(0, 7, "ESTIMATED SHOPPING BUDGET", ln=True)
    pdf.ln(2)
    pdf.set_font("TNR", "", 12)

    budget_items = [
        ("Smoke detectors (10-12 pack)", "$120 - $200"),
        ("CO detectors (3-4 units)", "$60 - $100"),
        ("Egress ladder", "$50 - $100"),
        ("Weatherstripping + door seals", "$40 - $80"),
        ("Garage door bottom seal", "$20 - $40"),
        ("Screen door latch", "$10 - $15"),
        ("Replacement shutter", "$30 - $80"),
        ("Bathtub stopper", "$8 - $15"),
        ("Cabinet hardware", "$10 - $20"),
        ("Pella parts (hardware + covers)", "$50 - $150"),
        ("Faucet aerators (x6)", "$18 - $48"),
        ("CLR calcium remover", "$5 - $8"),
        ("Silicone spray", "$8 - $12"),
        ("Light bulbs", "$15 - $30"),
        ("Spackle + paint", "$15 - $25"),
        ("Strike plates / latch hardware", "$20 - $40"),
    ]

    total_low = 0
    total_high = 0
    for item, cost in budget_items:
        pdf.cell(120, 6, f"  {item}", ln=False)
        pdf.cell(0, 6, cost, ln=True)
        low, high = cost.replace("$", "").split(" - ")
        total_low += int(low)
        total_high += int(high)

    pdf.ln(2)
    pdf.set_font("TNR", "B", 12)
    pdf.cell(120, 7, "  TOTAL ESTIMATED", ln=False)
    pdf.cell(0, 7, f"${total_low} - ${total_high}", ln=True)

    pdf.ln(4)
    pdf.set_font("TNR", "I", 10)
    pdf.multi_cell(0, 5,
        "TIP: Order Pella parts first \u2014 they may take 1-2 weeks to ship. "
        "Everything else is available at Home Depot / Lowe's. "
        "Bring photos of existing hardware/fixtures when shopping to ensure matches.")

    pdf.output(os.path.join(OUTPUT_DIR, "00_Contractor_Call_Cheat_Sheet.pdf"))
    print("Generated: 00_Contractor_Call_Cheat_Sheet.pdf")


if __name__ == "__main__":
    generate_calling_cheatsheet()
    generate_plumber()
    generate_electrician()
    generate_handyman()
    generate_mason()
    generate_siding_painter()
    generate_glass()
    print("\nAll PDFs generated in:", OUTPUT_DIR)
