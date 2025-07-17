<!-- PageHeader="25. 6. 10. 오후 1:42" -->
<!-- PageHeader="about:blank" -->


# ALLEGRO Solution Manual

BKD(Booking & Documentation) Booking Version 1.0

<!-- PageFooter="about:blank" -->
<!-- PageNumber="1/72" -->
<!-- PageBreak -->

<!-- PageHeader="25. 6. 10. 오후 1:42" -->
<!-- PageHeader="about:blank" -->


## 1. Overview


### 1.1. Module Feature

The work of Booking & Documentation is largely divided into 4 categories: Booking, Outbound
Documentation, Customs Manifest Declaration, and Inbound Documentation.

First, Booking reserves the vessel schedule and transportation route from cargo origin to the delivery
location together with equipment space to stuff cargo. Subsequently, it covers sending booking confirm
notices to the customer as well as depot and terminal. The scope of work also covers from managing
changes in booking information to vessel closing, which is to determine a shipment volume by
considering S/I receipt status, container gate-in status, and approval for special cargos in order to
facilitate a loading process.

Second, Outbound Document covers to input shipping instruction in written for Billing of Lading and
Cargo Manifest required to declare to the Customs, preparing operational documents such as a
Container Load List and special cargo details required for the export process, and Correction Advise to
handle B/L Data Amend after Document Closing time.

Third, Customs Manifest is used to declare to the customs authority accordingly to the requirements
of the customs regulations of each country.

Fourth, the scope of Inbound Documentation ranges from Arrival Notice, Transshipment, i.e. Next
connecting Vessel Voyage Assign and Confirm, production of inbound documents, i.e. container
discharge list and DG Manifest and up to the Cargo Release.

To cover all these, this manual is divided into 7 functions - Setup, Code, Booking, O/B Document, I/B
Document, Manifest and Operational Reports. Meanwhile, Setup and Code will be explained in the last
section.


### 1.2. Relationship of Module

<!-- PageFooter="about:blank" -->
<!-- PageNumber="2/72" -->
<!-- PageBreak -->

<!-- PageHeader="25. 6. 10. 오후 1:42" -->
<!-- PageHeader="about:blank" -->


<figure>
<figcaption>Figure 1BKG Process and interface</figcaption>

Customer
Portal

BKG/SI Request Info.

Biz. Revenue & Cost

CBP

EDI

Setup

Code

Inquiry VSL SKD

SKD

SCG
(Internal)

Special Cargo Loading
Request/Approval

BKG visibility info.
Creation & Renewal

Booking

MOV

FRC
(Internal)

Freight & Charge Data

Outbound
Doc

Inbound
Doc

Service Route select

SNM

Customs

Manifest.(IFM/OFM)

COD Request/Confirm

VOP

Advance
Manifest

Manifest

Door Move Request
Inq. WO Status

Terminal

TRX

CLL/CDL Info.

Port Auth.

DG Manifest

Operation

Report

Freight & Collection Status

FAR

Mail System

Booking Confirm

Demurrage /detention

DND

Fax System

Draft B/L Info.

A/N & H/N & P/N Info.

Container Movement Activity

MOV

EDI

</figure>


As you see in diagram, for Booking & Documentation process, a lot of sub-system are inter-related
each other.

Application of Booking Route will be acceptable only within the available service network management
in SNM and vessel schedules on SKD. When freighting, it is referred by Rate contract in FRC and its
result is transferred to the FAR for invoicing upon rating

As a booking & SI Receipt channel, it can be transacted from external parties, such as customer portal
and private EDI.

Based on the Booking/Documentation data, subsequent sub-systems can perform their function, such
as door move job order issue in TRX, AR invoice issue, CBP etc. as above


### 1.3. Function Description

Booking function consists of following menu structure


| Level 1 | Level 2 | Level 3 | Description |
| --- | --- | --- | --- |
| Booking | Booking | Work with Booking | To find the previous booking data with various search option not only "Booking No(B/L No) or P.O No but also "booking date, ETD duration' Vessel Voyage and Route or customer etc. and to execute next further job for the selected Booking No. |
|  |  | Booking Master | To create basic Booking Master data such as Vessel Voyage, route, shipper, container reservation type/size and quantity and to make additional data such as Special Cargo Also, able to search previous booking data and update information. |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="3/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

about:blank


| Level 1 | Level 2 | Level 3 | Description |
| --- | --- | --- | --- |
|  |  | Partner Lines SOC Booking & B/L Creation | To create Booking Master data and attaching container using excel file. |
|  |  | Booking Merge | Combining many booking numbers into one booking number. To merge bookings which POR or POL is different, "Hitchment" option is added. |
|  |  | Booking Split | Splitting a booking number to multiple booking numbers including special cargo request information. |
|  |  | e-Booking & S/I Service | Managing the E-Booking & S/I receipt and upload to the main Booking/Documentation system. |
|  |  | Door Move (Inland Haulage) Booking | Input Door move instruction and transfer to the TRX module |
|  |  | Container Information | Managing container number and other related information such as seal number, package, weight and measure. |
|  |  | Special Cargo (DG/RF/AK/BB) Job list | Finding the special cargo application with various search option and to execute further process such as Update and request. |
|  |  | Request Special Cargo | Special Cargo is classified into dangerous (Hazardous) cargo, reefer cargo and over-dimensional awkward cargo or Break-Bulk cargo loaded onto the Containerized Vessel for which special request. |
|  |  | DG Suspicious Booking Monitor / Verify | Monitoring DG Suspicious Booking No which has been detected during the S/I data input and to verify it by the compliance auditor |
|  |  | Booking Close for Bay Plan | To declare the Booking close for the specific Vessel Voyage and loading port for bay-planner to start their own job |
|  |  | Transmit Booking Fax/Email/EDI | To transmit Booking receipt or Draft B/L service to the Customer or other parties via fax/e-Mail or EDI |
|  |  | Booking Status Change | To change the Booking status (Waiting to Firm vice versa) in a group, referring to the important data related to slot control |
|  |  | VGM Dashboard | Monitoring the VGM data receiving status transferred through EDI and to confirm it to be fixed as B/L-Container VGM |


## 2. BOOKING

<!-- PageFooter="about:blank" -->
<!-- PageNumber="4/72" -->
<!-- PageBreak -->


## 25. 6. 10. 오후 1:42

<!-- PageHeader="about:blank" -->


### 2.1. General

Booking is the first activity to execute the shipping business physically which range from booking
request until vessel closing with receiving the shipping request from a customer. It is a customer service
area that involves the booking request of service route including vessel schedule and equipment space
from customer and confirm not only to customer but also to empty container release order to the
Depot/Terminal.

It is a series of activities from booking master data creation and to follow up the container movement
activity against the Booking information until vessel closing time. Also, receive the Shipping Instruction
in written (hereunder, S/I) from the Customer and hand it over to documentation dep't for
documentation staff to input S/I details required for B/L and operational document and manifest.

As first job, to make a booking master, following data such as Shipping Party, Vessel Voyage or
Expected Shipping Date, Booking Route (Place of Receipt, Loading Port, Discharge Port, and Place of
Delivery), commodity and estimated weight are required. Second, send booking confirmation notice to
the customer and update booking status and prepare the final loading list.

Meanwhile, in case of special cargo booking such as Dangerous cargo, Awkward (Out of Gauge) cargo,
Reefer and Break-Bulk cargo, additional applications is required through request/approval process
between customer service and vessel planner dep't for vessel operational safety.


### 2.2. Work with bookings

1\) Navigation: Customer Service > Booking > Work with Booking

2\) Screen Explanation

This window enables you to work with booking. Using this window, you can find the Booking No with
essential booking data in brief at a glance in various views. And go to next working step for subsequent
job process such as "Update", "Copy Booking ", "Copy B/L" "Split Booking", "Merge Booking", "Send
Email/Fax/EDI" etc by clicking on the respective execution button after selection of relevant Booking No
and also create new Booking Master.

3\) Work Process

Input search option and Click "Search"

4\) Item Explanation

<!-- PageFooter="about:blank" -->
<!-- PageNumber="5/72" -->
<!-- PageBreak -->

<!-- PageHeader="25. 6. 10. 오후 1:42" -->
<!-- PageHeader="about:blank" -->

Overview

ew To search the data following option should be given. If date option is given such as
'Booking (Booking Creation)/Onboard date and ETD (ETD of 1st Vessel POL), at least
one another item should be given together.

If ETD date is given, VVD or her calling port (Vessel POL= V.POL) should be given
together.

However, if individual Booking B/L No is given, data can be retrieved (other conditions
are ignored).

Category

Search
Key


| Item Name | Mandatory Explanation |  |
| --- | --- | --- |
| <Basic Search Option> At initial screen, only basic search options appear. |  |  |
| Date | √ :selected: | One of following date is required within Max.31 days |
|  |  | (1) Booking (Booking Master Creation) date or |
|  |  | (2) On board date (B/L Onboard Date) or (3) ETD date (1st Vessel Voyage/POL) |
| Vessel | √ :selected: | Actual VVD-Vessel Voyage/Direction (Including T/S shipment) together with POL |
| V.POL | √ :selected: | Vessel related POL |
| Booking No./ B/L No. | √ :selected: | Booking No./ B/L No. |
| Booking Office |  | Booking office |
| Staff |  | Booking staff ID |
| Status |  | F-Firm, W-Waiting, A-Advanced (Vessel is not fixed) and X-Cancelled Booking Status. In case of "ALL", cancel booking is excluded |
| LCL |  | LCL (Less than Container Load) (Yes / No) |
| FCL-Console |  | FCL-Console (Yes / No) |
| DPC |  | DPC (Document Process Close) Status (Yes / No) |
| SI |  | S/I Receiving Status (Yes / No) |
| <Detail Search> when you click detail search, following options appear additionally. |  |  |
| POR |  | POR (Place of cargo Receipt) where carrier's responsibility commences |
| POL |  | POL (Port of Loading- 1st Loading Port in case of T/S shipment) |
| POD |  | POD (Port of Discharge- Final Discharge Port in case of T/S shipment) |
| DEL |  | DEL (Place of Delivery) where carrier's responsibility ends. |
| DEL Continent |  | Continent of Delivery Location code (ALL / ASIA / EUROPE / AFRICA / AMERICA) |
| Booking Via |  | Booking Receiving channel of Booking Master such as Manual Creation, "INTTRA" GTN,WEB etc. |
| S/I Via |  | S/I receiving channel of Booking Master such as "INTTRA" GTN,WEB etc. |
| Loading OFC/Sales Rep. |  | Sales office (Loading Office)/Sales Rep. Code |
| Cargo Type |  | All-MTY Repo (All Except Empty Cargo) Laden (Full-F) |
|  |  | MTY SOC (Empty SOC Cargo-R) |
|  |  | MTY Repo (Empty Reposition for COC Cargo-"P") Bulk (Break Bulk Cargo-"B") ALL (F+R+P+B) |
| Special Cargo type |  | Special Cargo type (DG / AK / BB / RF / PC / SS) |
| EQ Type/Size |  | To filter the Booking by Container EQ type/size (eg,D4,D2,R2,R5 ... ) |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="6/72" -->
<!-- PageBreak -->

<!-- PageHeader="25. 6. 10. 오후 1:42" -->
<!-- PageHeader="about:blank" -->

Overview

v To search the data following option should be given. If date option is given such as
'Booking (Booking Creation)/Onboard date and ETD (ETD of 1st Vessel POL), at least
one another item should be given together.

If ETD date is given, VVD or her calling port (Vessel POL= V.POL) should be given
together.

Category

However, if individual Booking B/L No is given, data can be retrieved (other conditions
are ignored).

Grid-
result


| Item Name | Mandatory | Explanation |
| --- | --- | --- |
| Rating |  | Charged / Non Charged |
| Customer Ref No |  | (1) Kind of Reference Number (Drop down list box) placed on the Booking Master-"Reference No" and "P/O & Other No" on the "Marks & Goods" screen (2) Relevant Value input field |
| Contract No |  | Contract No of Booking Master |
| Customer |  | (1) Customer Type(drop down box-Shipper, consignee Etc) / (2) Customer Code -2 country digit + 6 number digit / Customer name (inquiry popup) |
| Partner SOC |  | Partner SOC (Yes / No) |
| Status |  | Booking Status (Advanced/Waiting/Firm/Cancel) |
| LCL |  | LCL (Less than Container Load) (Y/N) |
| FCL Console |  | FCL Console ( Y/N) |
| Booking No |  | Booking No.(You can open booking screen by double- clicking) |
| Via |  | BKG & S/I Receiving Channel (Off, Web, INT etc.) |
| Office |  | Booking Office Code |
| B/L No. |  | B/L No.(You can open booking screen by double- clicking) |
| B/L No. Type |  | Bill of Loading Number Type |
| Partner SOC |  | Partner SOC code |
| Shipper |  | Shipper name on the "B/L Customer" screen |
| Forwarder |  | Forwarder name on the "B/L Customer" screen |
| Trunk Vessel |  | Trunk VVD of Booking Master |
| 1st Vessel |  | First Vessel Voyage in the T/S Route of each booking |
| 1st Vessel ETD |  | 1st Vessel related POL ETD. |
| Container Volume |  | 20ft/ 40ft/ Total Box of Booking Container type/size |
| POR/ POL/ POD/ DEL |  | POR/POL/POD/DEL Code on Booking Master. |
| T/S Port (Pre / Post) |  | PRE: Pre relay Port of Trunk VVD and POST- Discharging Port from the Trunk VVD for next connecting Vessel in case of T/S. |
| SVC Type(ORG/Dest) |  | ORG-Cargo Receiving Term at ORG(Origin) and DST- Delivery Term at DST(Destination)ST(R/D) Term (eg, Y-CY, S-CFS etc) |
| BRN Sent |  | BRN(Booking Receipt Notice) Sent flag (Y/N) |
| Draft B/L Sent |  | Draft B/L Sent flag (Y/N) |
| Special Cargo |  | :selected: :selected: Kind of Special Cargo : (DG-Dangerous, RF-Reefer, AK-Awkward, BB-Break Bulk, RD-Reefer Dry, HG-Hanger bar Install, PC-Pre Caution, SS-Special Stowage) Definition of Flag Indicating flag has changed as per the data processing status: (1) "Y"-Marked as special cargo but not yet input any details or did not request-> (2) "R"- Requested -> (3) "A"-Approved or "N"-Rejected-> (4) 'C"-Canceled |
| Commodity |  | Rep. Code and exact Commodity Code of Booking main screen |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="7/72" -->
<!-- PageBreak -->

<!-- PageHeader="25. 6. 10. 오후 1:42" -->
<!-- PageHeader="about:blank" -->

Overview To search the data following option should be given. If date option is given such as
'Booking (Booking Creation)/Onboard date and ETD (ETD of 1st Vessel POL), at least
one another item should be given together.

If ETD date is given, VVD or her calling port (Vessel POL= V.POL) should be given
together.

However, if individual Booking B/L No is given, data can be retrieved (other conditions
are ignored).


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
|  | Contract No. |  | Contract No. When it shows "TEMP00001",it should be fulfilled by real Contract No for rating. |
|  | PO No. |  | PO(Purchase Order) No. for Customer reference |
|  | Rating |  | Indicates Rating status (Y/N) |
|  | S/I RCV./ Via |  | S/I(Shipping Instruction) Receipt Indicator/ receiving channel |
|  | DPC |  | DPC(Document Process Close) Time Passed or Not (Y/N) |
|  | Customer Ref. No. |  | Customer Reference No. |
|  | Cargo Type |  | Cargo Type(F: Laden/ R:MTY SOC/ P: MTY Repo /B: Bulk) |
|  | Sales Office |  | Sales Office which arrange the Booking at Loading Port |
|  | Sales Rep. |  | Sales Representative Code associated to the shipper. |


## 5) Button Explanation


| Category | Button Name | Explanation |
| --- | --- | --- |
| Action Key | [Create] | Open "Booking Master" screen to create booking |
|  | [Search] | Search Booking list with search condition |
|  | [Clear] | Initialize search condition |
|  | [Export Excel] | Download the displayed Booking list in Excel file |
|  | [History] | To trace the Booking (or B/L) amendment history |
|  | [Copy Booking] | To open "Booking Copy" screen with selected Booking |
|  | [Copy B/L] | To open "Copy B/L" pop-up |
|  | [Split Booking] | To split the "Booking No" |
|  | [Merge Booking] | By selecting multi booking no and clicking button, Booking merge screen pops up (Shipper code, route and VVD should be same) |
|  | [Cancel Booking] | To Cancel booking |
|  | [Send Email/Fax/EDI] | To open "Send Email/Fax/EDI" pop-up |
|  | [Detailed Information] | To open "Booking Master" screen with selected booking No. |


### 2.3. Booking Master


#### 2.3.1. Booking Master Creation

1\) Navigation: Customer Service > Booking > Booking Master


#### 2) Screen Explanation

This is a screen to key in basic booking information to create a booking master with Booking number,
which will become the basis of shipment information afterwards.

<!-- PageFooter="about:blank" -->
<!-- PageNumber="8/72" -->
<!-- PageBreak -->


##### 25. 6. 10. 오후 1:42

about:blank

To create a Booking Master, there are 8 mandatory items to be input placed on the left side with sky-
blue background color such as POR (Place Of Receipt), DEL (Place Of Delivery), Trunk VVD (or Sail Date),
Shipper, Contract Number, Commodity, Estimated Weight, Booking Volume per EQ Type/Size.

In case of special cargo like Dangerous, Reefer, Awkward and Break-Bulk, additional application job is
required after creation of Booking Master in advance.

In the meantime, If you have a pre-assigned booking number, user can create a booking master for own
office as contingency plan or china booking agent purpose by inputting a pre-assigned booking number.


#### 3) Work Process (Create and Search)

First. Input Route information - POR, DEL and respective Receiving/Delivery term as route and Sail
Due date. The other options such as POL and POD are not mandatory items and will be updated by
service network management (hereafter SNM). However, when Trunk Vessel/Voyage(hereafter T/VVD)
is used, POL and POD should be given as mandatory item

2nd, Input Shipper code. If freight forwarder codes are mapped to the shipper code in the Customer
file, it is automatically is provided while select the shipper code popup screen.

3rd, Input or select Rate Contract number. When you do not know the exact Contract No, type
"TEMP" for temporary purpose which means "undefined" for continuous booking process. Later on, you
can update it by real contract No at least before Rating time. At this time, when you click pop-up
button, proper contract No can be found by the name of customer.

4th, Input Commodity code. If Contract number is already input, you can choose commodity code
assigned to selected contract No.

5th, Input container Type/Size(hereafter TP/SZ) and required Quantity and estimated Total Cargo
weight in the Booking level

6th, If special cargo is involved like DG, RF, AK and BB , check at the associated column after click
special Cargo information.

7th, click "SAVE" button. If multiple service route is found, select proper route considering transit time
and cost.

Meanwhile, when you use pre-assigned Booking No, type Booking No into the Booking No field and
input booking data as mentioned above and click "Save"

<!-- PageFooter="about:blank" -->
<!-- PageNumber="9/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

<!-- PageHeader="about:blank" -->

<How to inquire the previous Booking Data>

There are three ways. Input booking number or B/L No or P/O No and click [Search] button
When you use "P/O No" as search criteria and multiple Booking Nos. are found with similar P/O No,
selection screen for correct Booking No populate.


#### 4) Booking Master inter-relationship with other Booking & Documentation jobs

When you look the top line right-upper side, you can see the series of button like [Master][Door
Move][Container][Ship. Party][Mark & Goods][C/M][Freight][B/L Issue][House B/L] [Switch B/L]. Those
are the Booking Master related screens required to "Door Move" and "Container" detail required at the
Booking time. And the others are the Documentation job related input screens from S/I input detail to
B/L Issue.

Those are so closely integrated from booking time, B/L information for O/B document, to entries for
B/L issue until B/L release so that a user can input relevant information in a consecutive order.

Meanwhile, you can trace the Booking and B/L data progress status based on the button coloring as
background change where are placed on the right upper hand at once (Sky blue color as back ground
indicates Data existence while white color shows no data which means no action so far and Orange color
means "Data Input is done but confirmation is not yet completed". Currently working screen indicates
orange color in square box.)

[Booking/Document Data Progress Status by coloring]


#### 5) UI item description (M-Mandatory Input, CM-Conditional Mandatory Input, D-Display item)


| General | To search the Booking Master, following three options are available |  |  |
| --- | --- | --- | --- |
| CategoryItem | Name | Mandatory | Explanation |
| Search Key |  |  | Booking Number as key number. When booking data is properly saved by the rule, it is provided from the system. |
|  | (1) Booking No. | :selected: √ | In case of using pre-assigned BKG No, check box appear in front of "Pre-Assigned Booking No." |
|  |  |  | When updating or inquiring about the existing Booking(B/L) data, it is used as one of the search keywords |
|  | (2) B/L No |  | Bill Of Lading Number. Once Booking No is created, the same number is used as B/L No. |
|  | (3) P/O No. |  | Input Purchase Order No. for customer reference. |
|  |  |  | When creating the Booking No, it can be input at the same time. Later on, it is also used as one of the Booking Data search keywords together with Booking No and B/L No. |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="10/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42
General

about:blank

Category


| To search the Booking Master, following three options are available |  |  |
| --- | --- | --- |
| Item Name | Mandatory | Explanation |
|  |  | -. If multiple booking numbers exist for a similar PO number, following "Select B/L No by the P/O No" will pop up. and select the B/L No what you want. |
| Booking Office |  | Booking Office |
| Staff |  | The ID of booking staff who received booking. If user click the ID, more information will be shown |
| Pre-Assigned Booking No. |  | Flag to use pre-assigned manual booking Number instead of auto-generated booking No. To assign booking number manually, "Pre-Assigned Booking No." indicator should be ticked |
| S/I |  | When Shipping Instruction is received, make sure to select "Yes" as evidence of receipt. In case of e-S/I, no need to tick because it is automatically indicated when e-S/I was received |
| Auto EDI Hold |  | Auto EDI Hold to prevent automatic EDI transmission |
| Split |  | Booking split status indicator. In case of memo B/L split, it indicates Memo(SH,AD) as per short/overland status |
| DPC |  | After Document Process Closing time is over, "Y" is displayed automatically |
| Booking Status |  | Booking Status (Firm/Advanced/Waiting/Cancel and Waiting Reason if waiting status) |
| <Route Information> |  |  |
| [Constraint] |  | POPUP - When SNM has constraint clause , it become to red color for reminder to check and among them if it is made by Link constraint it is moved to "Vendor Remark" |
| [View Milestone] |  | POPUP - To inquire Ocean Route Details and future transportation plan provided by SNM. |
| [Route Detail] |  | POPUP - To inquire/Update Ocean Route Details including T/S |
| POR | √ :selected: | Place of Receipt |
| POL | :selected: √ | Port of Loading (1st POL). When Trunk VVD is given, this is changed as conditional mandatory item |
| POD | √ :selected: | Pot of Discharge (Last POD). When Trunk VVD is given, this is changed as conditional mandatory item |
| DEL | :selected: √ | Place of Delivery |
| Receiving term Delivery term | :selected: √ | Cargo Receive & Delivery term (eg, Y/Y=CY/CY, Y-CY, D- Door, S-CFS, T-Tackle, I-Free In, O-Free Out) |
| Trunk Vessel | :selected: √ | There are two ways of filling out T/VVD - manual input or selection in SNM screen. |
| Sail Date | √ :selected: | Input estimated Ship date. Then will be used for choosing VVD in SNM (7days more or less available vessel will be selected) |
| <Others on right side in line with "Route Information> |  |  |
| SOC |  | SOC (Shipper's Own Cargo) indicator. |
| Partner | :selected: √ | In case of Partner lines SOC, type Carrier code as partner ID (eg, HJS- Hanjin Shipping, PIL-Pacific Intl Lines ) |
| [Set] |  | Execution Button. When click "set" if SOC checked and Partner ID typed, automatically inquire Shipper and Consignee from personal pre-defined data as per Partner SOC setup .. |
| Waiting Reason |  | Select proper Waiting Reason in case of Vessel space/EQ shortage, Commodity and Others. In case of Special Cargo and Cross-Booking, system automatically indicates. |
|  |  | > Reason of Waiting: SP: Special Cargo-Not Approval, CB: Cross Booking, VS: Vessel Space Problem, ES: Equipment Shortage, CM: Commodity, OT: Others), > Remark : If yes, type in detail. |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="11/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42
General

about:blank

Category


| To search the Booking Master, following three options are available |  |  |
| --- | --- | --- |
| Item Name | Mandatory | Explanation |
|  |  | > Definition of Cross-Booking : When Booking office belonging to User ID and POR related Sales Office are different each other, it is classified to "Cross-Trade Booking". In this case, only the user belonging to POR control office can change it to Firm status. |
| MTY Pick-up CY |  | Input MTY Pick-up CY/Facility (popup) |
|  |  | When click popup button next to "Empty Pick-up Facility", "Available Container status per Day" can be searched. |
| Pre Vessel Voyage |  | Pre Carriage Vessel Voyage connecting to T/VVD and PORT |
| MTY Pick-up Date |  | Input Empty Container Pick Up Date |
| Post Vessel Voyage |  | Post carriage Vessel Voyage from T/VVD and relay Port |
| MTY Door Arrival |  | The tab to display BKG contact of customer |
| Delivery Date |  | Input Delivery Date |
| SO No. |  | Input SO(Shipping Order) number used in Taiwan |
| Full Return CY |  | Input Full Container Return CY. If user do not input, SNM will provide preset value |
| Available Slot(TEU) |  | Available Slot(TEU) is displayed based on the VSC-Vessel Slot Control (Allocation minus current Booking Volume) |
| Allocation |  | Pop Up-Move to "Control Allocation by Main Office" screen when "Available Slot (TEU)" is not "N/A". |
| Trans. Mode |  | Trans. Mode (LINE / OWN) |
| Company |  | Trans. Mode company name. |
| Tel. |  | Phone number of Transportation Company. |
| <Contract Information> |  |  |
| Shipper | √ :selected: | Code and name of Shipper. |
|  |  | POPUP- To confirm the Sales Rep and Contact Point associated with, "Find Customer" sub-screen popup |
| Load Office |  | Display Loading Office / Sales Rep. Code related to the Shipper |
| Contract No. | √ :selected: | Input Contract No (Note: If undefined or unknown, may use "TEMP" for temporary code) |
|  |  | - Pop Up: Find the contract No by the customer name |
| Named Customer |  | Named Account for rating |
| Commodity | :selected: √ | Commodity code (Note: If undefined or unknown, may use "000000" for FAK-Freight All Kinds) |
| SOC Empty |  | Indicator of commercial Empty Cargo for SOC. |
|  |  | However, for inter-company reposition purpose, use "Empty Container Reposition Booking" in separate screen. |
| Forwarder |  | Code and name of Freight Forwarder |
| Consignee |  | Code and name of Consignee |
| Cust. Ref.# |  | Customer Ref. No. If you have additional reference no, you can input various kinds of Ref. no in the "Reference No" sub-screen |
| H/BL Filer | :selected: √ | In case of booking destined to US or CA, House B/L filer should be selected |
|  |  | (1- Carrier's Filing NVO, 2- Self Filing NVO. 3.Not Applicable) |
| Self Filer SCAC | :selected: √ | Input House B/L Self-filer SCAC (Standard Carrier Alpha Code) Code |
| [Detail] of Self Filer | :selected: √ | POPUP -Information from Self-AMS-Filing NVO |
| Booking Contact S/I Contact | :selected: √ | It consists of two kinds contact point for "Booking" and "S/I". Basically it comes from Shipper code selection |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="12/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

about:blank

General

To search the Booking Master, following three options are available

Category


| Item Name | Mandatory | Explanation |
| --- | --- | --- |
|  |  | stage as per Customer Contact profile, but direct input is also possible |
|  |  | < Input Item> Name, Tel., Fax, Email, Mobile Phone |
|  |  | -. BKG Contact : It is used for Booking Receipt Notice -. S/I Contact : It is used for "Draft B/L Notice |
| Booking Container Qty | √ :selected: | Type reserved Container type/size and Quantity |
|  |  | - Type/Size: Container Type/Size (eg,D4) |
|  |  | - Qty : Q'TY of Container (D4 X4) |
|  |  | - EQ Sub. (Incl. Reefer Dry) : In case EQ Substitution rule is applied for Rating purpose, input Rate Applicable Container type & quantity in accordance with the physical EQ to be provided |
|  |  | *If reefer container is provided but it is used for 'Reefer Dry cargo", type Dry CNTR type. Then "RD" indicates (eg, R5- D4) |
|  |  | - SOC : Type SOC Quantity in case of SOC (Shipper's Own Container) |
|  |  | [Add Row] add blank Row(Container Type/Size) |
|  |  | [Delete Row] delete selected Row(Container Type/Size) |
|  |  | Total Qty : Display Input Container type & Quantity in one row |
| Rate Qty Detail | :selected: √ | [ Rate Qty Detail ] POPUP : EQ type break-down information for Rating Purpose. When special cargo, EQ Substitution Rule, SOC and different commodity base rate is involved for one B/L, container type/size-q'ty should be break-down for accurate Rate calculation. Details, refer to the popup screen explanation |
| Flex Height |  | [ ] Flex Height Check Box- |
|  |  | Flexible Height Container ( 40ft High Cube) Acceptable Flag when booking staff request "40ft Standard" and release Empty Container from Depot (Mainly used in USA region |
| LCL |  | Check if LCL (Less than Container Load) for user reference |
| FCL-Console |  | Check if FCL-Console for user reference |
| Est. Total Cargo Weight | :selected: √ | Estimate Total Cargo Weight. When actual cargo weight for B/L level is input, it is replaced by actual weight |
| [Send Email/FAX/EDI] |  | POPUP- To send various kinds of Notice |
| [Copy Booking] |  | POPUP - Copy Booking screen |
| [Booking Split] |  | Move to "Booking Split" screen |


<Additional Information>

It consists of four categories (Special Cargo/ Special Instruction / Service Information
and Remarks) which are not frequently used. At initial stage, it is hidden. When you click
title label , working job sub-screen appear. Once data exists, it always appear for user to
see.

'Special Cargo" :

If special cargo exists, please click " special cargo" then appropriate input screen appear.

] [Danger]

POPUP - To input DG Application

<!-- PageFooter="about:blank" -->
<!-- PageNumber="13/72" -->
<!-- PageBreak -->


## 25. 6. 10. 오후 1:42

about:blank


| General | To search the Booking Master, following three options are available |  |  |
| --- | --- | --- | --- |
| Category Item Name |  | Mandatory | Explanation |
|  | ] [Reefer] |  | POPUP - To input Reefer Cargo Application |
|  | ] [Awkward] |  | POPUP - To input Awkward(Out-gage)Cargo Application |
|  | [Break Bulk] |  | POPUP - To input Break Bulk Cargo Application |
|  | Stowage |  | POPUP - To input Stowage Request |
|  | Hanger |  | POPUP -To input Hanger Bar Installation for G.O.H. |
|  | <Special Instruction> |  |  |
|  | ] Precaution |  | If the commodity is precaution cargo designated in MDM, "Precaution" will be automatically ticked. It the booking is needed to be handled as "precaution" cargo, user can also tick "precaution". |
|  | ] Hide |  | Hide indicator for reference when provide the Empty Container Release |
|  | Premium |  | If the customer value segment is top group, "Premium" will be activated. If premium is clicked, block stowage will become "HOT". |
|  | ] Food Grade |  | Food grade indicator for reference to provide the sound/clean container when empty container is provided |
|  | ] Rail Bulk |  | User can choose one of the rail bulk type by using dropdown button |
|  | Destination OCP |  | Destination OCP(Overland Common Point) if customer requires full Cargo delivery to OCP from Port discharge in account of customer's expense |
|  | - Service Information - |  |  |
|  | [SVC Mode & Route] |  | POPUP - Reference for statistics material and Block stowage |
|  | [Reference No.] |  | POPUP - Reference No. screen |
|  | [Cut Off Time] |  | POPUP - Cut Off time. Default value comes from the Service Network and setup condition |
|  | [Roll Over] |  | POPUP - When update VVD, history is kept and user can input the Roll-Over reason |
|  | <Remark> |  |  |
|  | Customer Remark |  | Input 'Remarks" associated with Customer. This will be reflected on the "Booking Receipt Notice" |
|  | Vendor Remark |  | Input 'Remarks" associated with Vendor such as Depot, Trucking Co etc. This will be reflected on the "Empty Container Release order Notice" |
|  | Internal Remark |  | Booking Internal remark Internal remark will not be printed on the any external documents |
|  | Transportation Remark |  | POPUP - To input/share the Door Move Job order related Remark between BKG staff(BKG) and Logistics staff (TRS) |


<Pop Up screen Explanation as Sub window of "Booking Master"


| popup | [Route Detail] : When Booking Data is properly created, SNM provides detail ocean route including T/S leg and inland transportation modes. In this screen, user can also update T/S route and VVD per shipment leg. If T/S remark needed at the origin side to be referred at T/S port, input at "Remark1(Origin) make use of is needed |
| --- | --- |
| Ocean Route- Grid | <Shipment Leg and inland route Mode> In T/S case, ship leg is provided by SNM. However, you can create/ or update it here by manual. For additional T/S due to vessel schedule irregularity, make additional row and input VVD/port. Also booking staff at origin side can input memo for T/S staff to refer about the transshipment. |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="14/72" -->
<!-- PageBreak -->


## 25. 6. 10. 오후 1:42

about:blank


| General | To search the Booking Master, following three options are available |  |  |
| --- | --- | --- | --- |
| Category | Item Name | Mandatory | Explanation |
|  | Seq. |  | Service Port and VVD Per ship leg. |
|  | POL | √ :selected: | POL / Terminal Code and calling Seq. No of Leg |
|  | POD | √ :selected: | POD / Terminal Code and calling Seq. No |
|  | Vessel Voyage | √ :selected: | VVD operated from POL to POD associated with leg |
|  | Vessel Name |  | Vessel Name of the VVD |
|  | Carrier |  | Indicates Carrier Code |
|  | Lane |  | Service lane code |
|  | M/F |  | Indicates Mother Vessel or CCA Feeder Vessel |
|  | OFT |  | Flag to indicate OFT(Ocean Freight Term) applying area and Arbitrary charge or ARB(OAR or DAR) applying area |
|  | POL ETD/POD ETA |  | It shows current vessel Schedule associated with VVD. However, sometimes you can see it is blank. It means that vessel does not call as originally planned. In this case, you have to check vessel schedule again and update correctly. |
|  | T/S Memo |  | Indicates if T/S Port Remark exists |
|  | Approval Ref. No. |  | Approval reference number. |
|  | T/S Type |  | Indicates T/S Type (Int'I TS, YRD/PRD TS, Domestic TS, Phase In/Out, Shaodi). It is arranged to cover the Chinese Yangz/Pearl River Delta TS type. |
|  | Ship Status |  | Indicates shipment status per leg (S-Shortship, A-Ahead ship, T-Transload) |
|  | Container |  | Container reference. |
|  | ROB |  | Retain On board flag. This is exceptionally used when cargo is ship-back with Retaining On Board status with different Voyage No in spite of same vessel. |
| Inland | Origin Inland |  | Origin inland transportation mode (Truck, Rail, Feeder, Barge, Rail/Truck, Barge/Truck, Feeder/Truck) between POR to POL. Basically it is provided by the SNM. but if necessary, can be adjusted. |
|  | Destination Inland |  | Destination inland transportation mode between POD to DEL |
| T/S memo | Origin Port Remark |  | If origin office leave note to the T/S port, it can be seen on the T/S working job screen |
|  | T/S Port Remark |  | When T/S Port memo is given, its result can be seen |


## 6) Button Description


| Category Button Name |  | Explanation |
| --- | --- | --- |
| Main | Constraints | By clicking "constraints" button, "SNM - constraints" screen will pop-up. If there is constraint information, the button will be colored in red |
|  | View Milestone | By clicking "View Milestone" button, "Service Network Inquiry" screen will pop- up. |
|  | Route Detail | When Booking Data has properly stored with Booking No, detail ocean route including T/S leg and inland transportation modes by SNM is created. In this screen, user can also update it |
|  | T/VVD - < Help for Code>. | Inquiry Vessel SKD and select V.V.D as T.VVD to booking creation screen To search vessel schedule, input anyone among vessel service lane, VVD, POL, POD. |
|  | "Find Customer" |  |
|  | Shipper | Shipper code can be input manually or through customer inquiry screen. By clicking pop-up button, below customer inquiry screen will pop-up It consists of three parts. Left Upper side box is used for Customer code and right-upper side box for Sales Office/Sales Rep. code associated with selected |
|  |  |  |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="15/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

about:blank


| Category | Button Name | Explanation |
| --- | --- | --- |
| Forwarder Consignee |  | shipper. below box is to manage the associated Contact information and Forwarder of the selected Customer code above |
|  |  | (Note) Contact Point information is used to send the Customer advisory like Booking Receipt and Draft B/L Notice. |
|  |  | Forwarder code can be inputted manually or through customer inquiry screen. By clicking pop-up button, customer inquiry screen(same with Shipper) will pop-up |
|  |  | Consignee code can be inputted manually or through customer inquiry screen. By clicking pop-up button, below customer inquiry screen will pop-up |
|  |  | Search: retrieve Customer information with search condition |
|  |  | Select: interface Customer information to Booking Creation screen |
|  |  | More: retrieve more Customer information |
|  |  | Export Excel: download customer in excel file |
| Contract No |  | Contract No input column& POPUP button to search Contract No .. |
|  |  | -. Input appropriate Rate Contract No. or |
|  |  | -. By clicking pop-up button next to the Contract No input field, select the respective Contract No after find the Rate Contract No. |
|  |  | [Search Contract No.] |
|  |  | < Screen Explanation> |
|  |  | This is used to find the Contact No based on the customer code. After input the customer code (or name) on the Booking Master screen, the codes already input are moved to this pop-up screen for search applicable Contract No. |
|  |  | <Input item for Search> |
|  |  | -. Service Scope: Service Scope area of origin/destination in the Contract |
|  |  | Ex) TPE: Trans-Pacific East bound |
|  |  | -. Shipper, or Consignee, or Contractor Customer Code ( As search key: Country code & Name is available) |
|  |  | -. Apply Date: Valid period of contract |
|  |  | -. Forwarder: Code and name of Freight Forwarder |
|  |  | -. Contractor: Code and name of Contractor Name |
|  |  | <Grid> |
|  |  | -. Customer Type: P: Contract Party, S: Shipper, C: Consignee |
|  |  | -. Customer Code/Customer Name: Customer's code and Name |
|  |  | -. Named Customer: Named account for rating |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="16/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

about:blank


| Category | Button Name | Explanation |
| --- | --- | --- |
|  |  | -. Contract Type: Contract, Agreement |
|  |  | -. Contract Number: Contract Number |
|  |  | -. Contractor: Contractor Name |
|  |  | -. Effective Date: Effective Date of Contract |
|  |  | -. Expire Date: Expire Date of Contract |
|  |  | -. Loading Office: Sales Office Code |
|  |  | -. Service Scope: Service Scope area of origin/destination in the Contract |
|  |  | <Button> |
|  |  | Search: search contract information with search condition |
|  |  | Select: interface selected Contract Noto the contract No field in Booking |
|  |  | Creation screen |
|  | Named Customer | [Search Named Customer] |
|  |  | < Screen Explanation> |
|  |  | This is used to find the Actual Customer Name based on the Contact No. and B/L No. |
|  |  | <Input item for Search> |
|  |  | -. Applicable Date: Valid period of contract |
|  |  | -. Name: Name of the Actual Customer. |
|  |  | -. Contract No .: Contract Number |
|  |  | -. B/L No .: Booking Number |
|  |  | -. Duration: effective time for Actual Customer. |
|  |  | <Grid> |
|  |  | -. Seq: Number Actual Customer for rating. |
|  |  | -. Code: Customer code |
|  |  | -. Actual Customer Name: Customer name |
|  | Commodity ->Contract Commodity popup | If Contract No. is inputted, relevant Contract commodity screen will pop-up. If no contract is inputted or commodity with tick mark, commodity code inquiries |
|  |  | based on MDM data will pop-up |
|  |  |  |
|  |  | Contract commodity pop-up: The commodities enrolled in assigned contract will be displayed unless tick at the 'commodity-[x]" |
|  |  | (Note) When you inquire with tick of "Commodity" on the top line, data source is changed from "Contract No" to "Master Data-Commodity" |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="17/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

about:blank


| Category | Button Name | Explanation |
| --- | --- | --- |
|  |  | Search: search commodity of contract information with search condition |
|  |  | Select: interface selected commodity to Booking Creation screen |
|  | Rate Qty Detail | This is used to determine the Rating application criteria based on the Cargo type and other conditions required by freight rating structure. So, if special cargo or different commodity per one B/L, it should be broken -down based on the Booking Container quantity on Booking Master. |
|  |  | <Factor of Rating Q'ty Application> |
|  |  | > Container Type/Size |
|  |  | > Cargo Type: DR-Dry, DG-Danger, RF-Reefer, AK-Awkward, BB-Break bulk, |
|  |  | > EQ Substitution: For instance, When customer request D2 but carrier provide 'D4" due to EQ shortage. Or Reefer Dry cargo |
|  |  | > SOC: If not SOC, leave it blank |
|  |  | > Commodity: When one Booking has two different commodity rate, different commodity should be broken down. |
|  |  | > Hanger Install Bar Type: Single, Double, Tripe is made when "Hanger" installation data is inputted |
|  |  | Add Row: add blank Row |
|  |  | Delete Row: delete selected Row |
|  |  | Save: interface Qty Detail to Booking Creation screen |
|  |  | -. No or only one special cargo marking in booking screen |
|  |  | -. EQ-Sub, S.O.C, RD(Reefer/Dry) only without any special cargo mark |
|  |  | -. If special cargo mark and EQ-Sub. S.O.C, RD mark exists at the same time, above screen will pop-up and users have to arrange the proper container type/size per cargo type to fit with the Rate Application. |
|  |  | -. In case of hanger bar installation booking for GOH(Garment On Hanger) cargo, total hanger bar volume per each Type/Size should be the same as the volume assigned in hanger screen |
|  | Type/Size | As a container type/size code, below type/size are used when input the Booking Quantity. For reference, please click "Type/Size" button column |
|  |  |  |
|  |  | Select: interface Type/Size to Booking Creation screen |
|  |  | Export Excel: download type/size list in excel file |
|  | Danger | The Request Special Cargo screen(dangerous tab) will show up For the detail use of the screen, please refer to special cargo application chapter |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="18/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

about:blank


| Category | Button Name | Explanation |
| --- | --- | --- |
| Reefer Awkward Break Bulk Stowage Hanger MTY Pick-up CY |  | If the application is fully approved, the button will be colored in blue |
|  |  | If part of the application is not approved, the button will be colored in red |
|  |  | The Request Special Cargo screen(Reefer tab) will show up For the detail use of the screen, please refer to special cargo application chapter |
|  |  | If the application is fully approved, the button will be colored in blue |
|  |  | If part of the application is not approved, the button will be colored in red |
|  |  | The Request Special Cargo screen(Awkward tab) will show up For the detail use of the screen, please refer to special cargo application chapter |
|  |  | If the application is fully approved, the button will be colored in blue |
|  |  | If part of the application is not approved, the button will be colored in red |
|  |  | The Request Special Cargo screen(Break Bulk tab) will show up For the detail use of the screen, please refer to special cargo application chapter |
|  |  | If the application is fully approved, the button will be colored in blue |
|  |  | If part of the application is not approved, the button will be colored in red |
|  |  | The Request Special Cargo screen(Stowage tab) will show up For the detail use of the screen, please refer to special cargo application chapter |
|  |  | If the application is fully approved, the button will be colored in blue |
|  |  | If part of the application is not approved, the button will be colored in red |
|  |  | The hanger bar installation screen will pop-up |
|  |  | Type Number of Container Quantity as per Hanger Bar installation type. |
|  |  | Carrier Hanger: Carrier's Expense Hanger bar install |
|  |  | Merchant Hanger: Merchant's account Hanger bar Installation. |
|  |  | The assigned volume per each Type/Size should not be larger than BKG volume of matched Type/Size. |
|  |  | If user inputs any information in this screen, the button will be colored in blue |
|  |  | By clicking pop-up button next to MTY Pick-up CY, "Search MTY Pick-up CY" screen will pop-up |
|  |  | Search: search Available Equipment information with facility code |
|  |  | Select: interface MTY Pick-up CY Information to Booking Creation screen |
|  |  | In Search MTY Pick-up CY Inquiry screen, empty container availability information of selected yard will be displayed as below screen |
|  | Full Return CY | In Search Return CY screen, Contact Person information of facility will be displayed as below screen |
|  |  | Search: search Return CY information with facility code |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="19/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

about:blank


| Category | Button Name | Explanation |
| --- | --- | --- |
| Service Continent Route & Mode |  | Select: interface Return CY Information to Booking Creation screen |
|  |  | By clicking this button, below service mode & route screen will pop-up |
|  |  | -. Service Continent Route: Sub Continent Code of Origin/Destination |
|  |  | -. Service Continent Mode: Service Mode of POR-POL Pair (or POD & DEL) |
|  |  | <Kinds of Service mode> : |
|  |  | CLO: Calling Port of Trunk VVD and Local Service to POR(or DEL) |
|  |  | CIP : Calling Port of Trunk VVD and IPI Service to POR(or DEL) |
|  |  | NLO : Non-Calling Port of Trunk VVD and Local Service to POR(or DEL) |
|  |  | NIP : Non-Calling Port of Trunk VVD and IPI Service to POR(or DEL) |
|  |  | CMB: Calling Port of Trunk VVD and MLB service from/to POR(or DEL) for USA service |
|  | Reference No | By clicking this button, below Reference No. screen will pop-up |
|  |  | If there's any information, this button will be colored in blue |
|  |  | " If user ticks "Copy To Remark" selected reference numbers will be displayed in "Customer Remark" of booking Master |
|  |  | Save: update reference no |
|  |  | Copy to Remark: interface reference number to external remark |
|  |  | By clicking "Cut Off Time", below screen will pop-up |
|  |  | [Save]: update Cut Off Time in the Manual Update Time field |
|  |  | <Data relationship with SNM> |
|  |  | (1) Type of Cut Off Time |
|  |  | -. Empty Pick Up date, Full cargo Cut off, Rail Receiving Date and Port Cut off time are provided automatically in the System Time field based on schedule, CCT setup by yard of SNM module. |
|  | Cut Off Time | - . S/I(Shipping Instruction)/Export Customs Cut-off and VGM cut-off time are defined as per the setup function in the BKD module. Those are shown on the "System Time" |
|  |  | (2) Notice: Ticked Item will be shown on Booking Receipt Notice. Default value whether to show or not is functional based on "Booking Receipt Notice & Draft B/L Setup" table under Setup menu |
|  |  | (3) Manual Update Time: If system time is wrongly calculated or necessary to adjust, users can input time manually. And manual time will be displayed on Booking Receipt Notice with priority to the system time. |
|  |  | (4) Updated by: User ID who input manual update time |
|  | Roll Over | When VVD is updated, "Roll-Over Information" will be colored in blue. |
|  |  | In this popup screen, more detail data such as "Reason of Roll-Over" and remarks can be described. |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="20/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

about:blank


| Category | Button Name | Explanation |
| --- | --- | --- |
|  |  | -. "Reason of Roll Over" : Select the type |
|  |  | -. "Remark" : Input as memo if additional remarks is required |
|  | Remark Template -. Customer -. Vendor -. Internal | By clicking pop-up button in the "Remark" grid, below template screen will pop- up to make frequently used remarks in advance. |
|  |  | By using this, you can store Frequently used remark for Customer, Vendor and internal purpose. |
|  |  | <Process> |
|  |  | -. Select Type to be used among Customer, Vendor, Internal purpose |
|  |  | -. Make a Title and Contents and "Save" |
|  |  | - Add Row: Add blank Row |
|  |  | - Delete Row: Delete selected Row |
|  |  | - Save: update remark template |
|  |  | - Select: interface remark of Template to booking creation screen as per assigned type |
|  | [Search] | Retrieve the stored Data |
|  | [Clear] | Clear (or Reset) the displayed data |
|  | [Copy Booking] | Copy the previous Booking Data with new Booking No. Details, refer to "Copy Booking" function (For Details, refer to separate explanation to be followed) |
|  | [Booking Split] | Booking No Split by the Customer Request or Service(memo) B/L Purpose |
|  |  | (For Details, refer to separate explanation to be followed) |
|  | [History] | To trace the Booking (or B/L) amendment history (For Details, refer to separate explanation to be followed) |
|  | [Preview B/L] | View B/L Image (For Details, refer to separate explanation to be followed) |
|  | [Issue C/N] | View the all of C/N Issue History associated with the B/L. If DPC time is not over, it shows inactive. After DPC, it will be activated to allow C/N Issue |
|  | [Cancel] | Cancel the Booking No. Once cancelled, no more used in the future and Booking Status code become to "X" which is inactive as data. |
|  | [Firm to Waiting] <- > | Booking Status Change execution. |
|  |  | When Booking Data is created/update, booking status code will be made with "F"-Firm or "W"-Waiting as per the Cargo Specification or Cross-Trade Booking or others. |
|  | (Waiting to Firm) | To change it, this is used. In case of "W" status, button name is changed to "Waiting to Firm" vice versa. Meanwhile, original B/L Printing is blocked under "W-waiting Booking status. Therefore, all of Bookings should be clear to Firm before vessel closing time. |
|  | [Save] | Save input (or Update) Data. |
|  | Find Service Network | POP UP. If there are multiple ocean route in case of booking creation or route/VVD change, Find Service Network screen will pop-up for user to select proper route |
|  |  | This consists of four parts. |
|  |  | First, upper box shows available ocean route in order by low cost and short Transit time |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="21/72" -->
<!-- PageBreak -->


## 25. 6. 10. 오후 1:42

<!-- PageHeader="about:blank" -->


| Category | Button Name | Explanation |
| --- | --- | --- |
|  |  | 2nd, left middle box shows the current empty status EQ inventory per yard 3rd, right middle box show the Cargo Cut-off time. |
|  |  | 4th at bottom box show the Inland Transportation mode and estimated Transit Time and Cost. |
|  |  | Grid Explanation Grid Explanation |
|  |  | 1. Flag : Standard->Guide |
|  |  | 2. Priority : it is decided by S/N, considering under As per S/N |
|  |  | 3. [More]: There are numerous routes in S/N. Among them, practicable routes appears with internal rule such as "to show under priority 3 and within 2 T/S. If you want to another routes, click "More" |
|  |  | Sub- Button |
|  |  | [Full Route]: Search detail route and event as milestone from empty container release to deliver full cargo to the destination |
|  |  | [Constraints]: Show Constraint information of selected route |
|  |  | [Select]: interface selected Route to Booking Creation screen |
|  |  | Note: If there is only one ocean route in booking creation or route/VVD change, booking will be created/saved without pop-up SNM |
|  |  | . Detailed explanation below :selected: |
|  | [Waiting -> Firm] | Changing booking status from waiting to firm. If waiting reason is "Special cargo non approval", booking status will not be changed until vessel planer desk's approval. |
|  |  | In case of waiting due to Cross-booking, the person belonging to POR controlling office can change to "Firm". |
|  | [Firm -> Waiting] | Changing booking status from firm to waiting. The waiting reason will be "Others", if booking status is changed by this function |
|  | [Booking Split] | Move to "Booking Split" screen with current booking No. Detail explanation, please refer to the "Booking Split" |


### 2.3.2. Copy Booking

1\) Navigation: Customer Service > Booking > Booking Master (Popup)

2\) Screen Explanation

This is used to create the new Booking record in a mass based on the specific Booking No existed in the
Booking Data base. There are two kind of method. One is for generating the Automatic Booking No.

2nd way is made with pre-assigned manual Booking No.

<!-- PageFooter="about:blank" -->
<!-- PageNumber="22/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

<!-- PageHeader="about:blank" -->


## 3) Work Process

Open the Booking Master screen and input the target booking number as search key and "Search"
Click [Copy Booking] button. Then "Copy Booking" screen is opened as above

Type Number of Copy and select Copy type of Numbering between "Automatic No, Pre-Assigned No"
When you choose "Manual Copy", Manual Booking No Input boxes will appear instead of "New Booking
No."

Select Copy Options: When other special inform is also copied, take tick mark into the appropriate
column. if no need to copy, un-tick

Finally, Click "Copy Booking". Then New Booking Master Record is made with given Booking No.


### 4) Item Explanation


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
| Search | Booking No(B/L No) | √ :selected: | Original booking number: The copy source booking number |
|  | Number of Copy | √ :selected: | Type the BKG quantity that you want to copy. |
|  | Numbering Type | √ :selected: | Way of Booking Copy Type (Auto Assign, Manual Input) -. Automatic No .: System give the Number |
|  |  |  | -. Pre-Assigned No .: Input pre-assigned Booking No. into Manual Booking No field at bottom side. |
|  |  |  | (To know "How to get the pre-assigned manual Booking", refer to the "Manual Booking No" in the Set Up section) |
|  | Contract No |  | Contract No of original Booking No appears as default. If user changes contract No., changed contract No. will be assigned to new bookings |
|  | Copy Option |  | Supplemental Data Including Indicator: The title that has data will be activated and if not, inactivated. The tick-marked titles will be copied to new bookings. If user unselects some of activated titles, they will not be copied to new bookings |
|  | New Booking No / Manual Booking No | :selected: √ | It is changed depending on the "Copy Type". |
|  |  |  | -. Automatic No: New Booking Number - After "Copy Booking", new numbers are assigned. By double clicking the number, booking master screen will be linked |
|  |  |  | -. Pre-Assigned No: Manual Booking Numbers. Once select the " Pre-Assigned No", Input fields are arranged. On that field, Input Pre-Assigned Booking No into "Manual Booking No" field |
| Button | [Export Excel] |  | download route information in excel file |
|  | [Clear Data] |  | Initialize the screen |
|  | [Copy Booking] |  | Action key to make a new booking record with new Booking No. |


#### 2.3.3. Vessel SKD & Code

<!-- PageFooter="about:blank" -->
<!-- PageNumber="23/72" -->
<!-- PageBreak -->


## 25. 6. 10. 오후 1:42

about:blank
1\) Navigation: Customer Service > Booking > Booking Master (POPUP)

2\) Screen Explanation The screen for checking vessel schedule


## 3) Work Process

Input reference condition and search


### 4) Item Explanation


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
| Search | Lane |  | Input lane. The VVD schedule of the same lane will be listed |
|  | Vessel Voyage | √ :selected: | Input VVD. The schedule of the inputted VVD will be listed |
|  | POL |  | Input POL. The VVD schedule of the same POL will be listed |
|  | ETD |  | Input ETD. The VVD schedule during the inputted ETD will be listed. |
|  | POD |  | Input POD. The VVD schedule of the same POD will be listed |
|  | ETB |  | Input ETB. The VVD schedule during the inputted ETB will be listed. |
| Grid- result | Lane |  | Lane Code |
|  | Vessel Voyage |  | Vessel Voyage Code and Name |
|  | POL/Terminal |  | POL Code |
|  | CCT |  | Cargo Closing Time |
|  | ETB |  | ETB(Estimated Time of Berthing) of POL |
|  | ETD |  | ETD(Estimated Time of Departure) of POL |
|  | POD/Terminal |  | POD Code |
|  | ETB |  | ETB(Estimated Time of Berthing) of POD |
|  | Remark |  | Remark of each Vessel Schedule |
|  | Update Date |  | Update Date |


## 5) Button Explanation


| Category | Button Name | Explanation |
| --- | --- | --- |
| Main | Search | Search Vessel Schedule with search condition |
|  | Export Excel | Download Vessel Schedule in excel file |
|  | Select | Select Row |


### 2.4. Partner Lines SOC Booking & B/L Creation

1\) Navigation: Customer Service > Booking > Partner Lines SOC Booking & B/L Creation


#### 2) Screen Explanation

This is another way of Booking master creation for the partner lines SOC booking No and container No
list in pre-defined excel file format each other. It consists of three parts. One is the SOC Partner set up,
2nd is the Booking No creation and 3rd is the Container No attachment function.

<!-- PageFooter="about:blank" -->
<!-- PageNumber="24/72" -->
<!-- PageBreak -->


##### 25. 6. 10. 오후 1:42

about:blank

One is the "SOC Partner" basic information set up On this function, Port and Partner line contact party
which is used as shipper/consignee can be pre-defined per Partner Line and Port

By using pre-defined excel format, when user takes "Upload Excel" and click "Create Booking", Booking
Master data is created with Booking No


##### 3) Work Process

Set up "SOC Partner" to define the customer per partner line and port (Once setup, no more to re-
define it. When you do not make this, shipper/consignee code should be filled out in excel upload file)

Create the Booking Master. by Upload Excel file (Note: Format should be followed by Template) and
click

"Booking Creation"

When you received excel file, Attach the Container No. by Upload Excel file Then system automatically
find the relevant Booking No based on the Vessel Voyage/Partner and POL/POD and container details is
appended. For excel upload format, refer to Template.


###### 4) Item Explanation


| CategoryItem | Name | Mandatory | Explanation |
| --- | --- | --- | --- |
| Booking Master Creation |  |  |  |
| Search | Booking Creation Date | √ :selected: | Booking Ceation Date by using the Excel Upload function (Max. One month is available) |
|  | Type |  | Result of Upload File (All, Success, Fail) |
| Grid | Sequence Number |  | Sequence Number |
|  | Vessel Voyage | √ :selected: | Vessel/Voyage/Direction (VVD) |
|  | Booking |  | Booking No. After Booking creation process it will be shown |
|  | Result |  | Success or Fail. If mandatory items are not valid, fail appear |
|  | Container No. |  | Container number . (Min. 4 alphabet+7 Numeric) |
|  | Container Type/Size | :selected: | -. Min. one type/size is required |
|  |  |  | -. Type Booked Number of Container into the respective type/size field ( 20 Dry/40 Dry/40HC/45HC/20RF/40RF/20DG/40 DG/20 AWK/40 AWK) |
|  |  |  | (Note) Mapping condition about the container type/size can be customized per carrier's policy |
|  | TEU Total |  | Not is use |
|  | Weight (Kg) | √ :selected: | Esatimated Total Weight of this Booking No |
|  | Cargo Type | :selected: √ | Cargo Type (F- Full, M-Empty |
|  | Partner Line | :selected: √ | Carrier Code in Master Data |
|  | POL | :selected: √ | Port of Loading |
|  | Terminal POL |  | POL Terminal |
|  | POD | :selected: √ | Port of Disacharge related to the given VVD |
|  | Terminal POD |  | POD Terminal |
|  | Receiving Term | √ :selected: | Keep the Allegro Receive Term (Y-CY, I-Free In,T-Tackle ) |
|  | Delivery Term | :selected: √ | Keep the Allegro Delivery Term (Y-CY, O-Free Out, T-Tackle ) |
|  | Reference No. |  | Partner Lines own Refeence No. to represent Booking No level |
|  | UN NO |  | UN No. for DG cargo |
|  | IMO CLASS |  | IMO Class for DG cargo |
|  | TEMP |  | Temp for reefer container |
|  | Commodity Group |  | Commodity Group |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="25/72" -->
<!-- PageBreak -->


#### 25. 6. 10. 오후 1:42

<!-- PageHeader="about:blank" -->


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
|  | O/H,O/L,O/R,O/F,O/A |  | Overdimension status |
|  | Rate Contract No |  | Rate Contract No. If not arranged, it it regarded as "TEMP" |
|  | Shipper | √ :selected: | Shipper code. If SOC Partner is pre-defiend, no more need. However, if it is different from set value in the "SOC Partner", this input value is applied priorior to setting value. |
|  | Consignee | √ :selected: | Consignee Code. If SOC Partner is pre-defiend, no more need and POD related customer code is selected as Consignee. |
|  | Created User |  | Booking Master Creation User ID |
|  | Create Date |  | Booking Master Creation Date |
| Button | [Report] |  | SOC Booking Upload Report Data Pop Up when upload is failed |
|  | [Delete] |  | Delete Row |
|  | [SOC Partner] |  | SOC Partner setting |
|  | [Template] |  | Template file to be used as Upload excel |
|  | [Upload Excel] |  | To upload excel base Container List file |
|  | [Create Booking] |  | Final action key to create Booking Master after upload file |


## 2.5. Booking Merge

1\) Navigation: Customer Service > Booking > Booking Merge


### 2) Screen Explanation

The screen merges multiple booking numbers into 1 booking number. Basically, the combination can
be done on condition that VVD, Shipper, POL, and POD are the same. Once merged, other booking
numbers can no longer be used since the booking status for the numbers becomes cancel. Meanwhile, in
order to merge bookings whose POR or POL is different, "Hitchment" option is required in additionally.


### 3) Work Process

#1. Select "Booking B/L No." or "By Vessel Voyage & Route" (When you select "Booking B/L No.", "Add
Row" and "Delete Row" button will be activated. Please input the target Booking No to be merged by
making an input data row.

#2. When you take an option of "By Vessel Voyage & Route", Input first VVD together with POL/POD
and "Search"

#3. Choose bookings to be merged and click "Merge" button.

#4. Select Master booking and click "Merge"


### 4) Item Explanation


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
| Main- Search | > Option1. Booking B/L No. | :selected: √ | Booking B/L No: The option to input booking numbers manually |
|  | > Option2. By Vessel Voyage& Route |  | By Vessel Voyage & Route: The option to search bookings By Vessel Voyage & Route |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="26/72" -->
<!-- PageBreak -->


### 25. 6. 10. 오후 1:42

<!-- PageHeader="about:blank" -->


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
|  | First Vessel Voyage | √ :selected: | First VVD input column. The bookings that have the same first VVD will be listed when merge type is "By Vessel Voyage & Route" |
|  | POL | √ :selected: | Port of Loading when merge type is "By Vessel Voyage & Route" |
|  | POD | √ :selected: | Port of discharging when merge type is "By Vessel Voyage & Route" |
|  | POR |  | Place of Receipt |
|  | DEL |  | Place of Delivery |
|  | Hitchment |  | Hitchment cargo option. |
|  |  |  | To merge bookings whose POR or POL is different but loaded on the Same Vessel/voyage, tick "Hitchment" and proceed with merge process if POD, DEL and country should be the same. |
|  | Shipper |  | Shipper input column. The bookings of the inputted shipper will be listed |
| Grid | [ V ] (Checkbox) | √ :selected: | Check target Booking No to be merged. |
|  |  |  | Booking No: The assigned container volume |
|  | Status |  | Booking status such as waiting or firm |
|  | B/L No. |  | B/L number |
|  | Shipper |  | Shipper name |
|  | Trunk Vessel/Voyage |  | Trunk Vessel/Voyage |
|  | BKD Qty |  | Booking QTY from booking master |
|  | Cnt Volume |  | Container QTY attached to booking |
|  | Sales Office |  | Sales office code |
|  | Booking Office |  | Booking office code |
|  | POR/POL/POD/DEL |  | Route |
|  | Named Customer |  | Named account for rating |
|  | Rating Y/N |  | Status of rating |
|  | DPC |  | Status of DPC(Document Process Closing) |
|  | B/L Release |  | Status of OBL release |
|  | [Add Row] [Delete Row] |  | When "Booking B/L No" is selected as search key, it will be activated to make new row or delete one. |


#### 5) Button Explanation


| Category | Button Name | Explanation |
| --- | --- | --- |
| Main | [Search] | To inquire the target data to be merged. |
|  | [Clear] | Clear screen |
|  | [Merge] | Action key to merge the selected Booking Nos. When click it, below "Master Booking Selection" screen will pop-up |
|  |  | <Process> |
|  |  | - Select master booking to represent and click "Merge" to complete booking merge |
|  | [Container] | The container information of the selected Booking No for reference purpose. |


## 2.6. Booking Split

1\) Navigation: Customer Service > Booking > Booking Split

<!-- PageFooter="about:blank" -->
<!-- PageNumber="27/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

about:blank


### 2) Screen Explanation

The screen is used to split one booking number information to multiple bookings. Booking Number Split
is creating new booking numbers by splitting one booking number into more than two multiple booking
numbers either to split a B/L based on customer's request or to issue a service(memo) B/L resulted from
carrier's operational irregularity like short-ship or ahead shipment.

And coverage of Data split is Booking Container Q'ty including Rating purpose Q'ty, Total piece count,
Total measure, Total weight per B/L and Container No. In case of special cargo involvement, it also can
be split.


### 3) Work Process

Select "Split type" considering whether it is caused by Customer Request, or by carrier's operational
mistake required for Service(Memo) B/L for manifest purpose

<Case1 - Customer Request>

Input booking No with "Customer" as split type and click "Search" button. The first grid data will be
displayed.

Input the number of bookings to split booking and click "Split" button.

Modify container volume and containers associated with split booking No.

Assign special cargo application in case of special cargo booking with split booking No.
To Finish booking split, click "Save".

<Case2 - Memo(Service) B/L>

Input booking No with "Customer" as split type and click "Search" button.

Update Trunk VVD and check Short ship or Ahead ship into the relevant Container No
The other is the same as Customer Request.


#### 4) Item Explanation


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
| Main | Route, |  | Displayed POR, POL, POD, DEL code of the booking. |
|  | Indicator- Stowage , Hanger, Stop Off, Bulk Rail, Premium, Hide, Food Grade, Precaution, Remark |  | At the top right of the screen there are Split Option Indicators. If there's inputted data, the matched column will be ticked and copied to new booking. If the user deletes tick mark, it will not be copied |
|  | Split type | √ :selected: | Split type: 2 types. 1) Customer: Normal split to make new B/L 2) Service(memo) B/L: Split to make service B/L. Officially there is only one B/L in customer's hand and newly created bookings will be used as operational purpose internally for customs manifest purpose |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="28/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

about:blank


| CategoryItem | Name | Mandatory | Explanation |
| --- | --- | --- | --- |
|  | Split Number | √ :selected: | The number of booking to split. |
|  |  |  | -. Customer Request: Input the Numbers including the Original B/L. |
|  |  |  | (Max: 100) |
|  |  |  | -. Service B/L: Input the number as many as service in terms of actual shipment required to manifest(Max: 100) |
| Grid- Original Booking | >Original Booking |  | The information of source booking -. Booking number: Display item |
|  |  |  | -. 1st Vessel Voyage: Display item |
|  |  |  | -. Trunk VVD: Display item |
|  |  |  | -. Weight/Package/Measure: Display item |
|  |  |  | -. Service Network : Booking Route |
|  | >Split section |  | When No. of Split is given, Split Booking No row is made as many as given No sequentially. |
|  |  |  | It consists of three box to be updated. One is general data breakdown by Split No which shows Trunk Vessel Voyage/Weight/Package/ Measure, 2nd is for Booking Quantity and 3rd is to assign Container No. to each split booking No. (only if Container No. is already assigned to the original booking) |
|  |  |  | If Special Cargo data exists, mapping UI relevant to DG/RF/AK/BB appear at the bottom. The activated columns can be updated manually |
|  |  |  | <Upper Box : Split Bookings> |
|  |  |  | -. 1st Vessel Voyage: Display item |
|  |  |  | -. Trunk VVD: Once changed, "Select" button in "Service Network" column will be activated |
|  |  |  | -. Weight/Package/Measure : Editable item |
|  |  |  | -. Service Network: When Trunk VVD is changed, Select button is activated for verification. |
|  |  |  | <Left bottom Box : Booking Container Q'ty per cargo type> |
|  |  |  | -. Split Booked EQ Type/Size and Q'ty per Split Booking Sequence. |
|  |  |  | <Right bottom Box : Container No Information> |
|  |  |  | -. Container No : Tick mark to the relevant split booking No |
|  | Special Cargo Application Split |  | If the original booking has special cargo application, it can be split into bookings as assigned in below screens. If the container is assigned in special cargo application, it will follow container assignment. |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="29/72" -->
<!-- PageBreak -->


##### 25. 6. 10. 오후 1:42

<!-- PageHeader="about:blank" -->


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
| Service B/L | Service(Memo) B/L Split |  | When make a Service B/L, followings are different |
|  |  |  | (1) Original Booking No - Booking Status is changed to "S" for Split Master for Customer's on hand and it is no more used for manifest purpose while service B/L is workable to the operational report for CLL/CDL and Manifest |
|  |  |  | (2) While split, define which B/L and which container is related to "shortship" or "Advanced Ship" against the orginally intended the vessel in view of customer hold original B/L. The other is the same. |


## 5) Button Explanation


| Category | Button Name | Explanation |
| --- | --- | --- |
| Main | [Search] | Retrieve original booking information. |
|  | [Split] | Auto split function. Booking data such as weight and package will be automatically divided to split section |
|  | [Save] | Final Confirm key to complete "Split" |


### 2.7. e-Booking & SI Process

1\) Navigation: Customer Service> Booking >e-Booking & S/I Service > e-Booking & S/I Process


#### 2) Screen Explanation

This is the screen to search the e-Booking or SI request list received via various channel such as direct
EDI with VIP customer, Web, regional VAN and International Customer Portals and to upload it to main
database of Booking and to upload S/I (Shipping Instruction) against the given Booking No.


#### 3) Work Process

<Creation Stage>

Prepare the "Set Search" condition which will be frequently used as search criteria.

Set 'Request Date' with other option to retrieve and click "Search".

Select the target e-booking no with new status of "Booking" as Doc. type and click "Preview" for review.
Then, booking details can be viewed.

When you click "Upload" after select the target data or double-click, Upload job screen pop-up.

Compare e-Booking data and main Booking data input screen. If coding job is required to create Booking
master like Shipper/Sales Rep./ Vessel Voyage code or Commodity code etc., make sure to convert it to
fit

<!-- PageFooter="about:blank" -->
<!-- PageNumber="30/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

about:blank

Finally, Click "Upload".

If you want to reject due to overbook or other reason, click "Reject".
For Update, review seq. No next to the Request No and take Upload action.

Basic process the same as above
☒


## 4) Item Explanation


| Category Item Name |  | Mandatory | Explanation |
| --- | --- | --- | --- |
| Main | Request Date | √ :selected: | e-Booking or S/I received date |
|  | Upload Status |  | Status value (N-New, P-Pending, F-Confirm) |
|  | Handling Office |  | Handling Office is automatically assigned by booking office, sales office of shipper code, POR or POL location code. (Sales office code is converted into relevant booking office code, if e-Booking & SI controlled offices is registered in Office Set-up table under Setup menu) |
|  | Set Search POPUP |  | If clicking "magnifying icon" next to Set search and save data in pop-up screen and flag in this field, you can retrieve e-Booking & SI request(s) that match with set search option |
|  | [Detailed Search] |  | To give the detail search option, click here |
|  | [Search] |  | Search function key |
|  | Here under [Detail Search], each field is functional as 'Search" option as well as "Display Data" in the Grid |  |  |
|  | Request No |  | e-Booking & SI request number assigned by customer |
|  | Booking No |  | Booking No. In case of Booking Request, it is blank while S/I show it |
|  | B/L No. |  | B/L No registered in the Booking Master |
|  | Request Status |  | C-Creation, U-Update, X-Cancel |
|  | Clear button |  | Clear (or Reset) the displayed data |
|  | Vessel Voyage |  | Vessel/Voyage/Direction Code |
|  | Lane |  | Vessel Service lane related to the V.V.D of the Booking |
|  | Origin Country |  | 2 alphabet Country code of POR Location code |
|  | Delivery Continent |  | Continent code of DEL Location code |
|  | Via |  | e-Booking & S/I receiving channel such as Web, EDI, GTN, INTTRA and etc. |
|  | POL /POD /POR /DEL |  | Route |
|  | China Agent Code |  | 2 Digit Code for North China Booking Agent |
|  | P/O No |  | Purchase Order No assigned by customer |
|  | Document Type |  | Documentation Type. Booking, S/I (It is called S/R too) and B/L Check |
|  | EDI ID |  | EDI Trade Partner ID |
|  | Upload Office |  | Office code of user ID who made upload |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="31/72" -->
<!-- PageBreak -->


## 25. 6. 10. 오후 1:42

about:blank


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
|  | Customer |  | Customer Type / 2 alphabet code / 6 number digit / name |
|  | E-Mail |  | Customer Email Address |


### 5) Button Explanation


| Category | Button Name | Explanation |
| --- | --- | --- |
| Main | Agent EDI | To upload flashfile base Agent detail file. |
|  | Upload File | To upload excel base Booking detail List file |
|  | Customer Mapping | This is a mapping table between customer portal site own code in INTTRA/GT-nexus and ALLEGRO code. When upload by e-BOOKING from INTTRA, no need to input Allegro code as shipper if map is done. mapping code process e-booking customer mapping search & add & delete |
|  | Export Excel | Downloads the Result Grid Data in excel file |
|  | Pending | This is to process unclear requests within e-Booking & S/I process due date |
|  | Delete | This is to clear duplicated request without sending reject EDI message |
|  | Reject | When clicking "Reject", e-Booking & S/I reject is open to select reject reason and send reject notification email to customer |
|  | Preview | If selecting Seq. and clicking "Preview" button, you can view, print and save e-Booking Request or e-S/I Request in your local PC |
|  | Upload | When clicking "Upload", e-Booking & S/I tab is open as follows in order to upload e-Booking or S/I request information into Allegro system |
| Button (After Booking Selection) | Copy Option | If booking is already created, copy option screen automatically pops up to select tab(s) you want to update with e-booking or S/I information |
|  | Reinstate | State initialization, activated only when upload status is F, R, D |
|  | Pending | This is to process unclear requests within e-Booking & S/I process due date |
|  | Reject | When clicking "Reject", e-Booking & S/I reject is open to select reject reason and send reject notification email to customer |
|  | Upload | When clicking "Upload", e-Booking & S/I tab is open to upload e-Booking or S/I request information into OPUS system |
| Tab1 | Booking Tab |  |
|  | Booking Data ALLEGRO |  |
|  | Booking Data ALLEGRO | Current Booking Information existed in the Allegro based on the Booking No. |
|  | Go to Booking | To link the Booking Master screen |
|  | Booking No | Booking Number |
|  | Booking Status | Booking Status (Firm/Advanced/Waiting/Cancel and Waiting Reason) |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="32/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

about:blank


| Category | Button Name | Explanation |
| --- | --- | --- |
|  | Route Information |  |
|  | Trunk Vessel Voyage | There are two ways of filling out T/VVD - manual input or selection in P/C screen. By clicking pop-up button, below screen will pop-up. |
|  | POR | Place of Receipt |
|  | POL | Port of Loading (1st POL) |
|  | POD | Pot of Discharge (Last POD) |
|  | DEL | Place of Delivery |
|  | Pre | Trunk VVD previous port on Booking |
|  | Post | After Trunk VVD on Booking port |
|  | Final Destination | If the final destination of the cargo is indicated and also requested on the B / L as described on L / C |
|  | Sailing Due Date | Estimated Ship date. Then will be used for choosing VVD in S/N (7days more or less available vessel will be selected) |
|  | R/D Term | Cargo Receive & Delivery term (eg, Y/Y- CY/CY) |
|  | Return Date | The date on which the Empty Container in Outbound is expected to arrive at the location designated by the shipper in the Container Yard |
|  | Freight Term | Freight term code for re-handling charge - P: added to PREPAID - C: added to COLLECT |
|  | Delivery Date | Delivery due date |
|  | Full Return Facility | Full Container Return Facility. If user do not input, S/N will provide preset value |
|  | Pick-up Date | Container Pick Up Date |
|  | Pick-up Facility | Input empty Pick-Up Facility (popup) When click popup button next to "Empty Pick-up Facility", "Available Container status per Day" can be searched up to 14 days -Details. |
|  | Trans Mode | Transportation Mode between Customer's own trucker or Liner's one. |
|  | Company Code | Transportation Company Code |
|  | Company Name | Transportation Company Name |
|  | Tel. No. | Transportation Company Tel. No. |
|  | SHPR (Shipper) | Shipper code can be input manually or through customer inquiry screen. By clicking pop-up button, below customer inquiry screen will pop-up |
|  | Forwarder | Forwarder code can be inputted manually or through customer inquiry screen. By clicking pop-up button, below customer inquiry screen will pop-up |
|  | Loading Office | Display Loading Office |
|  | Contract No | Contract No. input column. By clicking pop-up button, below Contract No. search screen will pop-up |
|  | HS Code | Harmonized System code |
|  | Commodity | Commodity. input column. By clicking pop-up button, below |
|  | H/BL Filer | In case of booking destined to US (or CA), House B/L filer should be selected if NVOCC booking with |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="33/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

about:blank


| Category | Button Name | Explanation |
| --- | --- | --- |
|  |  | involving house B/L. |
|  | Self Filer SCAC | When NVOCC files House B/L by himself, type NVOCC Standard Carrier's Alpha Code. |
|  | Estimated Weight | Estimate Total Cargo Weight. It can be replaced by actual weight based by B/L |
|  | Type/Size | Container Type/Size |
|  | Volume. | Container volume per TP/SZ |
|  | EQ Substitution(Including Reefer/Dry) | The column to assign EQ Sub TP/SZ and Vol - Assign EQ Sub TP/SZ and Vol - EQ Sub volume per each TP/SZ should not be larger than BKG volume of matched TP/SZ. |
|  | Shipper's Own container | The column to assign Shipper's Own container volume - Shipper's Own container volume should not be larger than BKG volume of matched TP/SZ |
|  | Special Cargo |  |
|  | Dangerous | dangerous cargo indicator |
|  | Reefer | reefer cargo indicator |
|  | Awkward | awkward cargo indicator |
|  | Break Bulk | break bulk cargo indicator |
|  | Hide | Hide indicator |
|  | Precaution | Precaution indicator |
|  | Food Grade | Food grade indicator |
|  | Flex Height | Flexible Height indicator, use both D4/D5 |
|  | Auto Notification | Automatic Notice flag about the Booking Receipt Notice, Draft B/L, Waybill etc. FAX / Email |
|  | Additional Information |  |
|  | Contact Information | If it is flagged, booking confirmation or draft B/L is automatically emailed to customer after uploading. -Contact Info: If you flag "copy from e-service", contact information from e-service is updated BKG Contact updated BKG Contract: BKG contract of customer - S/I Contact: The tab to display S/I contact of customer. |
|  | Reference No | External request identification number |
|  | Document Requirement | Document Requirement |
|  | Remark | It is copied to "Remark" in Booking Data Allegro |
|  | From e-Service |  |
|  | From e-Service | Information received from customer via e-Service channels |
|  | Booking No/B/L No. | Booking Number |
|  | Req. No. | External request identification number |
|  | Via | Reception channel |
|  | No. of H/BL | No of H/BL |
|  | Upload | Whether the booking is generated |
|  | Req. Status | Booking Status reflected |
|  | Upload Status | Update status |
|  | Type | Type of received data |
| Tab2 | Shipping Party Tab |  |
|  | Shipper | Either can manually input, or can search by using "B/L Customer" pop-up screen |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="34/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

about:blank


| Category | Button Name | Explanation |
| --- | --- | --- |
|  | Type | When customer code is inputted, the concerned name and type (B: BCO / N: Non-BCO) registered in MDM will be automatically displayed next to the code field. |
|  | Name Address | Either can manually input, or can copy MDM data by using 'reset' button when Customer Code is available. |
|  | Print | When clicked, the address will be printed on Bill of Lading |
|  | City/State Country Zip Code Street/P.O/Box | City/Country is mandatory when the BKG POD is Canadian Port or Canadian FROB. |
|  | EORI No. | Report number to European customs |
|  | USCC(China), Tax ID | Reference number to China customs |
|  | Tel./ Fax / E-mail | Required to input for Arrival Notice when available |
|  | FMC No | Mandatory when Freight Forwarder is involved in the business for US |
|  |  | export shipment |
|  | Same as Consignee | When clicked, Consignee's Name & Address data will be copied in. |
| Tab3 | Container Tab |  |
|  | Status | Movement status of the container. |
|  | Container No | Container number input column. If the container number is not enrolled in |
|  |  | container master, it will not be inputted. |
|  | Type/Size | Container Type/Size |
|  | SOC | Shipper's Own Container |
|  | Seal No. | Seal No |
|  | Package | Package number and unit contained in each container |
|  | Weight | Weight contained in each container |
|  | Measure | Measure contained in each container |
|  | Receive Term Delivery Term | Cargo Receive & Delivery term (eg, Y/Y- CY/CY) |
|  |  | Cargo Receive & Delivery term (eg, Y/Y- CY/CY) |
|  | Partial | Partial indicator. If container volume is smaller than 1, it will be flagged |
|  |  | automatically (User cannot unflag it) |
|  | S/I | To show the Shipping Instruction. |
|  | [Copy To ALLEGRO] | reset data received from e-Service |
|  | [Delete Row] | Delete selected Row |
|  | [Cancel Copy Data] | Delete copied data received from e-Service and display Allegro data |
| Tab4 | Mark & Description Tab |  |
|  | Package | Package number and unit contained in each container |
|  | Weight | Weight contained in each container |
|  | Print | Indicator to indicate whether to include at the time of B/L output |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="35/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

about:blank


| Category | Button Name | Explanation |
| --- | --- | --- |
|  | Measure | Measure contained in each container |
|  | Freight Term | Prepaid / Collect |
|  | Rep. Goods Description | Type representative Cargo Description |
|  | HS Code | Harmonized System code |
|  | Marks & Number | Marks & Number |
|  | Description of Goods | Description of Goods |
|  | No. of Package/Container | Total No. of Package/Container in Word |
|  | Export Information | Export Information |
|  | P/O Other No. | This is the integrated screen to input/manage VIP Customer's Internal |
|  |  | Shipping Reference No. such as P/O No., Invoice No. etc. |
|  |  | This is provides 2 types of input section. The 1st section is to input |
|  |  | reference no. by BKG level (upper part of the screen). The 2nd is to input |
|  |  | P/O no. by CNTR or Item level |
|  |  | P/O No. (by BKG): Each P/O No from Booking (or B/L) P/O No. (by CNTR): P/O No from CNTR |
|  | C/M by Booking Tab |  |
| Tab5 | Container No. | Container No. attached to the BKG |
|  | Seq | Container Manifest sequence number |
|  | Description of Goods | Cargo Description of Goods |
|  | Package | Input piece count of the item |
|  | Weight | Input weight of the item |
|  | Measure | Input volume of the item |
|  | HS Code | Mandatory in case of MYPKG T/S |
|  | HTS Code | Mandatory in case of US FROB, In-transit or T/S |
|  | Marks | Marks & Numbers - US / Canada manifest file no. for House B/L |
| Tab6 | Door Move tab |  |
|  |  | Door Move |
|  | Seq. | Number order |
|  | Status | Status value of door Move - Canceled |
|  |  | - Confirm - Frustrate |
|  | Bound | bound information(in/out bound Code) |
|  | Haulage | Subject of inland transportation |
|  | Type/Size | Container Type Size |
|  | Return - Yard | Container return facility |
|  | Return - Date | Container return date |
|  | Pick-up - Yard | Container pickup facility |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="36/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

about:blank


| Category | Button Name | Explanation |
| --- | --- | --- |
|  | Pick-up - Yard | Container pickup date |
|  |  | Multi - Stop |
|  | Seq. | Number order |
|  | Door Arrival Date | Door Arrival date and time |
|  | Location | Location information By clicking this button, below screen will pop-up. |
|  | zone | Zone information By clicking this button, below screen will pop-up. |
|  | Actual Customer | Door Address By clicking this button, below screen will pop-up. |
|  | Zip Code | ZIP Code of Door location |
|  | Address | Door Location Address |
|  | Contact - Name | Name of the carrier |
|  | Contact - Phone No. | Phone number of carrier |
|  | Contact - Email | Email of carrier |
|  | Remark | Remark |
|  | [Copy To ALLEGRO] | reset data received from e-Service |
|  | [Delete Row] | Delete selected Row |
|  | [Add Row] | Row add |
|  | [Copy Row] | Copy selected Row |
|  | [Cancel Copy Data] | Delete copied data received from e-Service and display Allegro data |
| Tab7 | Reefer Tab |  |
|  | No | Number order |
|  | Container No. | Container numbers |
|  | Type/Size | Container Type/Size. TS should be inputted even if container number is not assigned |
|  | Commodity | Item classification code By clicking this button, below screen will pop-up. |
|  | Temperature | RF container temperature setting. |
|  | Genset | Gen set usage mark |
|  | Ventilation | Ventilation setting. |
|  | Nature | The nature of cargo. Nature can be selected in drop down list |
|  | Humidity | Humidity percentage input column. |
|  | Remark | Type remark . |
|  | Status | An indicator indicating whether the port is authorized. |
|  | [Copy To ALLEGRO] | reset data received from e-Service |
|  | [Delete Row] | Delete selected Row |
|  | [Cancel Copy Data] | Delete copied data received from e-Service and display Allegro data |
| Tab8 | Dangerous Tab |  |
|  | No. | Number order |
|  | Container No. | Container numbers |
|  | Type/Size | Container Type/Size. TS should be inputted even if container number is not assigned |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="37/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42
Category

about:blank


| Button Name | Explanation |
| --- | --- |
| Seq. | Sub sequence for dangerous goods in the same container serial no. |
| UN No. | By clicking pop-up button, below "IMDG Code Inquiry by UN No." will pop- |
|  | up. UN No. should be inputted through pop-up screen. If not, other |
|  | information such as IMDG Class and proper shipping name will not be updated. |
| IMDG Class | IMDG Class |
| Proper Shipping Name | Proper Shipping Name |
| Technical Name | Hazard contents |
| Flash Point | If IMDG Class or Sub Label is 3, flash point should be inputted |
| Packing Group | Packing Group |
| Marine Pollutant | Whether marine pollutants |
| Gross Weight | Gross weight input column. If gross weight is smaller than net weight, the |
|  | input will not be accepted |
| Limited Qty | Limited Q'ty status input column |
| Net Weight | Net weight input column. Net weight should not be larger than gross weight |
| Cargo Status | Select cargo status by selecting from drop down list |
| Emergency Contact No. | Emergency contact phone number. Mandatory item |
| Remark | Type remark |
| [Restrictions] | By clicking this button, below screen will pop-up. |
| Status | An indicator indicating whether the port is authorized. |
| [Attach File] | Attachments |
| [Copy To ALLEGRO] | reset data received from e-Service |
| [Delete Row] | Delete selected Row |
| [Pre Checking Report] | Pre-Checking Report |
| [Cancel Copy Data] | Delete copied data received from e-Service and display Allegro data |
| Awkward Tab |  |
| No. | Number order |
| Container No. | Container numbers |
| Type/Size | Container Type/Size. TS should be inputted even if container number is not |
|  | assigned |
| Commodity | AK cargo commodity basically follows booking commodity. This commodity |
|  | can be changed if needed. |


Tab9

<!-- PageFooter="about:blank" -->
<!-- PageNumber="38/72" -->
<!-- PageBreak -->


## 25. 6. 10. 오후 1:42

about:blank


| Category | Button Name | Explanation |
| --- | --- | --- |
|  | Length(cm) | Input cargo dimension information. |
|  | Width(cm) | Input cargo dimension information. |
|  | Height(cm) | Input cargo dimension information. |
|  | Package | The number of packages |
|  | Gross Weight | Gross weight of cargo. It should not be smaller than net weight. |
|  | Net Weight | Net weight of cargo. It should not be larger than gross weight. |
|  | Remark | Type remark if yes. |
|  | Status | An indicator indicating whether the port is authorized. |
| Tab10 | House BL Tab |  |
|  | Seq. | Sequence No. |
|  | House B/L No. | NVOCC's House B/L No. |
|  | Actual Shipper | Input actual shipper information of H.B/L |
|  | Actual Consignee | Input actual consignee information of H.B/L |
|  | Actual Notify | Input actual notify information of H.B/L |
|  | Mark & Nos | Shows Marks & Numbers data of H.B/L if it's transmitted via EDI |
|  | Weight | H.B/L weight of the item |
|  | Package | H.B/L piece count of the item |
|  | Measure | H.B/L volume of the item |
|  | Description | Shows Description data of H.B/L if it's transmitted via ED |
|  | Container No. | Container No. attached to the BKG |
|  | Type/Size | Container Type/Size. |
|  | Package | Input piece count of the item |
|  | Weight | Input weight of the item |
|  | Measure | Input volume of the item |
|  | Marks | Marks. and No. |
|  | Description of Goods | Cargo Description of Goods |
|  | HTS Code | Mandatory in case of US FROB, In-transit or T/S |
|  | NCM Code | Mandatory in case of MYPKG T/S |
|  | [Cancel Copy Data] | Delete copied data received from e-Service and display Allegro data |
|  | [Copy To ALLEGRO] | reset data received from e-Service |


### 2.8. Door Move (Inland Haulage) Booking

1\) Navigation: Customer Service> Booking >Door Move (Inland Haulage) Booking


#### 2) Screen Explanation

This is the screen to make the door move (Inland Haulage) instruction data not only by Carrier
Haulage but also by Merchant Haulage for logistics dep't staff to issue Job Order to the inland trucking
company. And it is used for empty container delivery to pick up the cargo at loading port (Outbound) as
well as Full Container release at destination (Inbound)

In Merchant Haulage case, Door Address and Haulage Charge section disappeared and it replaced by "Drop Off Charge

<!-- PageFooter="about:blank" -->
<!-- PageNumber="39/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

<!-- PageHeader="about:blank" -->


#### 3) Work Process

Input mandatory item related to Door delivery per Container type/size as many as the Number of
required Container (it is changed depending on the haulage Type among Carrier's Haulage and
Merchant's Haulage)

In case of Carrier's Haulage, please clarify whether transport cost will be covered under the Rate
Contract or not. If it covers, take "Yes" as manifest Rate in the Haulage Charge. Otherwise, select "No" as
not manifested rate which means IHC should be rated here.

If non-manifest rate, Input receivable amount into "Non-Manifest Rate".

Click "Confirm" for logistics staff to start job order to instruct the trucker with J/I creation in TRX
module.

Once J/O has been taken by logistics dep't, Cancelation is not allowed before withdrawal by the logistics
part in TRX. So, in this case, user have to contact the person in charge of Job Order.

If actual transportation job has been under processing but customer want to stop further transportation
service, take "Frustrate" after select the target container seq. no.


## 4) UI Item Description


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
| Basic Information | Booking No/ BL Number | √ :selected: | Booking No/ BL Number as search key |
|  | Bound | √ :selected: | Indicator of Outbound (or Inbound). Based on this, mandatory item to input is changed |
|  | [Open] or [Close] |  | To see brief booking information about the route/VVD for reference, click here. Then reference information appear |
|  | Customer |  | Customer Code & Description (Outbound - Shipper and Inbound-Consignee appear) |
|  | Return Yard (or |  | According to bound type, the information is changed |
|  | Pick up Yard) |  | (Outbound : Return Yard / Inbound : Pick up Yard) |
|  | Container Information: |  |  |
|  | Grid on right upper side shows the summary of working results for reference |  |  |
|  | -. Type / Size |  | Container type/size of target container to work. |
|  | -. Qty |  | Total Container quantity to be booked as Target. |
|  | -. Carrier Haulage |  | Total Q'ty of Carrier haulage. |
|  | -. Merchant Haulage |  | Total Q'ty of merchant haulage |
| Data Input Fields |  |  |  |
| Door Move (Inland | Seq. |  | Number sequence |
| Haulage) Instruction - Grid- | Bound |  | Inbound - I, Outbound - O |
|  | Haulage | :selected: √ | Select between Carrier Haulage and Merchant Haulage. By Haulage type, mandatory items are automatically changed. |
|  | Mode |  | Transportation Mode (Truck, Rail, Barge). If blank, it means "All kind of mode". If you want specific transportation mode, please select in list box. |
|  | Actual Customer Name |  | Pop Up Button: When you registered Customer Door move related information as under in "Named Customer" in TRX |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="40/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

about:blank


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
|  |  |  | module, following Customer Name/address/contact point can be picked up. |
|  |  |  | > Navigation: [TRX module] Code=> Manage Named Customer |
|  | Zone | √ :selected: | Door move haulage zone |
|  | Door Arrival Date |  | Date to pick up full container |
|  | Address |  | Address |
|  | Zip Code |  | Zip Code |
|  | Contact |  | Contact Point |
|  | Pick-up Yard / Date | :selected: | Empty Container Pick up yard / date (O/B), But in case of I/B, its meaning is changed to Full Cargo Pick Up |
|  | Return Yard /Date | :selected: | Full Container return yard / date for O/B, Empty Container Return Yard/Date for I/B |
|  |  |  | -. In case of Merchant's Haulage, it is mandated |
| Container Information | Seq | √ :selected: | Number sequence |
|  | Status | √ :selected: | Working status of Container No. It is changed by the execution button |
|  | Multi Stop |  | Multi stop for stuffing container <Muti Stop: Y> Open the grid : Door Address & Contact Point -. Seq: Number sequence. |
|  |  |  | -. Zone: Door move haulage zone |
|  |  |  | -. Door Arrival Date: Door arrival date -. Actual Customer Name: Actual customer name |
|  |  |  | -. Zip Code: Zip code of the door address |
|  |  |  | -. Address: Door address |
|  |  |  | -. Contact: Contact information(name/telephone/email) |
|  | Slot |  | Container Slot number |
|  | Type/Size | √ :selected: | Container type/size |
|  | Container No. | √ :selected: | -. In case of outbound cargo, no need to input Container No. -. But, in inbound case, it should be specified accordingly per "CNTR Seq. |
|  |  |  | -. If you click "magnifying icon", "Search Door Move Container" popup is displayed and you can select one of them. |
|  | Cargo Weight(KGS) | :selected: | Cargo weight |
|  | Load Ref. |  | Load Reference |
|  | Special Cargo Seq. |  | If special cargo application data exists, a corresponding data sequence no. is mapped (DG Seq: DG Cargo Application, RF Seq. Reefer , AK-Awkward ) |
|  | Commodity | √ :selected: | Commodity code |
|  | Rep. Commodity |  | Representative commodity code related to the commodity code |
|  | Multi-B/L |  | Whether Multi-B/L or not. (Y/N) |
|  | Remark |  | The remark of haulage |
|  | Confirm |  | Confirm user / date. Once confirm, it is shown |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="41/72" -->
<!-- PageBreak -->


## 25. 6. 10. 오후 1:42

about:blank


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
|  | Job Information |  | Job Instruction number / date. When Job Order is issued in TRX module, its result is shown. Also, when J/O is issued, cancel or any Data update is not allowed. |
| Haulage Charge | This data is required only for the Carrier's Haulage. |  |  |
|  | Manifested Rate(Y/N) | √ :selected: | Specify whether haulage charge is manifested as All-In Rate of "OFT" in the rate contract or not. If yes, no more need to input Haulage cost. Otherwise, make sure to input in the Non Manifest Amount column. |
|  | Currency | √ :selected: | The currency of haulage charge or Additional Charge |
|  | Manifested Amount |  | Manifested amount. If Contract covers as All-In rate, leave it blank |
|  | Non-manifested Amount | √ :selected: | Non-manifested amount. If Manifested Rate Flag is "N", make sure to input. After input here, this amount will be interfaced to the "Freight & Charge" screen with the charge of "OIH" for O/B and "DIH" for I/B |
|  | Additional Charge/Amount |  | Type Addition revenue amount with Currency such as BAF. |
|  | VAT(Y/N) |  | Value Added TAX for shipment. It is automatically reflected in invoice. |
|  | T1 Document(Y/N) |  | Travel Document Required or not. It could be differently named per region. |
|  | Customs Clearance No. |  | Customs clearance number |
| Drop Off Charge | This is required in case of "Merchant Haulage" |  |  |
|  | Manifested Rate(Y/N) | √ :selected: | Specify whether haulage charge is manifested as "OFT" in the Contract or not. |
|  | Currency | √ :selected: | The currency of haulage charge |
|  | Manifested Amount | √ :selected: | Manifested amount |
|  | Non-manifested Amount | √ :selected: | Non-manifested amount |
|  | VAT(Y/N) |  | Value Added TAX for shipment. It is automatically reflected in invoice. |


## 5) Button Description


| Category | Button Name | Explanation |
| --- | --- | --- |
| Top | [Search] | Search Door Move information with B/L No |
| Door Move Inland Haulage Instruction | [Add/Delete Row] | Add or Delete row to grid. |
| Container Information | [Show Cancel Status] | To show the status of the canceled Slots. |
|  | [Add Row] | Add row to grid. |
|  | [Delete Row] | Delete row to grid. |
|  | [Copy Row] | Copy selected row to grid. |
|  | [Cancel] | Cancel selected row |
|  | [Confirm] | When you click "Confirm" button, confirm screen will pop up to decide payer party and collection responsible office. In this screen, please make sure to Haulage Cost collection Office. Then, non-Manifested Amount will be interfaced to the "Freight & Charge" screen in case of "DIH" for I/B. |
| Bottom | [History] | To trace the Booking (or B/L) amendment history |
|  | [Preview B/L] | Upon selecting Seq. and clicking "Preview" button, you can view, print and save Door Move(Inland Haulage) Booking in your local PC |
|  | [Issue C/N] | View the all of C/N Issue History associated with the B/L. If DPC time is not over, it shows inactive. After DPC, it will be activated to allow C/N |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="42/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

<!-- PageHeader="about:blank" -->


| Category | Button Name | Explanation |
| --- | --- | --- |
|  |  | Issue |
|  | [Danger] | The button for "Request Special Cargo Dangerous Tab" for reference |
|  | [Reefer] | The button for "Request Special Cargo Reefer Tab" for reference |
|  | [Awkward] | The button for "Request Special Cargo Awkward Tab" for reference |
|  | [Copy D/I] | -. Copy D/I information to another B/Ls. |
|  | [Send Email/Fax/EDI] | To open "Send Email/Fax/EDI" pop-up |
|  | [Save] | Save Door Move information. |


### 2.9. Container Information

1\) Navigation: Customer Service>Booking>Container Information>Container Information

2\) Screen Explanation

The screen is divided into 3 sections. The box two on the upper side displays the result of "Total
Quantity Comparison" to check the discrepancy between Booking Master and Container details in B/L
level.

And the section of "Each Container Information below is the actual screen to input data, such as
Container No, Seal number, piece count, weight, measurement, and special cargo flag etc.

It is used as a source information for documents, such as B/L, Container Load/Discharge, and
Manifest.

Meanwhile, when Container Gate activity occurred in MOV(Movement) management sub-system,

physical Container No. flows into this screen until confirmation and latest movement status is updated
until ID-Inbound delivery for easy cargo tracking service.


#### 3) Work Process

Check whether Container No coming from Container Gate Out/In activity is correct or not against the
S/I (Shipping Instruction). If unmatched, Input container number.

Input other information such as Seal number, package, weight etc. related to the Container No

Check the balance whether the Container quantity specified on the S/I matches the Container quantity
against that in Booking Master. If unmatched, update Booking Quantity as many as that in S/I

Check sum of Package, Weight and Measure per each container No is equal to that in the B/L level, using
"Total Quantity Comparison" grid

If all in good order, make sure to click "Container Confirmation" in order to block data flow in from
Movement or fix the Container No list necessary to CLL(Container loading List)

Meanwhile, If Container No is used as part load together with other B/L(s) under same VVD and POL,
type the occupied ratio with decimal point into the "Occupy" column as much as shared volume. Or use
"Part Load/Move" function.

<!-- PageFooter="about:blank" -->
<!-- PageNumber="43/72" -->
<!-- PageBreak -->

<!-- PageHeader="25. 6. 10. 오후 1:42" -->
<!-- PageHeader="about:blank" -->


## 4) Item Explanation


| Category | Item Name | Mandatory Explanation |
| --- | --- | --- |
| <Each Container Information - Input items |  |  |


Input items
This box is the input screen for the Container No and its related data. Whenever Container
No is added/updated, the comparison result show at the upper side (See detail, below-
comparison result)


| [ ] Select |  | Select Box for "Delete Container", "Container Confirmation", |
| --- | --- | --- |
| No. |  | Sequence No of the Container No. |
| Slot |  | Empty Container Slot to attach container |
| Container No | √ :selected: | Input "Container No." When Gate In/Out activity is done through the "Container Movement" by manual input or EDI processing, it flows to here together with event code/date/event yard |
| Status |  | Movement status code. (eg, OP,OC,VL,TS.VD.IC.ID,MT). When user input the "Container No" here, MT appears. However, when movement activity are properly taken, current status as of searching time appear together with "Event occurred place and time at "Origin Yard" and "Event Date" field respectively. |
| Type/Size | √ :selected: | Container Type/Size relevant to the "Container No." -. In case of COC, it appears as per the Container Master spec. -. However, in SOC case, make sure to input proper type/size |
| Seal Count |  | Count of Seal Number |
| Seal No.1 (Seal No2) |  | The first seal number and 2nd Seal Number |
| Kind/Code |  | Select Seal kind and sealer code. The codes and details are as below: |
|  |  | < Seal Kind> : M - Mechanical seal, E - Electronic seal < Sealer =Sealing By> CA - Carrier, SH - Shipper, AA - Consolidator, CU - Customs, AB - Unknown, AC - Quarantine Agency, TO - Terminal Agency |
| Multiple Seal No |  | If seals are more than 3, input more seal number in the pop- up screen by click magnifier glass button next to the "Seal No" |
| Package |  | Package Piece Count and Unit contained in each container |
| Cargo Weight |  | Cargo Weight contained in each container |
| R.Ton |  | Revenue ton. |
| VGM Weight |  | VGM(Verified Gross Mass) which is transferred from VGM dashboard via EDI |
| Measure |  | Measure contained in each container |
| Occupy | √ :selected: | -. It always indicates "1" for FCL case which cargo occupy the container usage. 1 means 100% exclusively use. -. For part load case with other Bookings, its occupied ratio should be filled out up to 2 digit decimal point relevant to this Booking No.(eg, If 35% shared, type 0.35 instead of percentage) Then, Partial column is changed to 'Y" |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="44/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

about:blank


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
|  |  |  | Validation Rule: When same container no is used under the same Trunk VVD /POL/POD, it becomes to mandatory item. |
|  | R/D term | √ :selected: | R/D(Receive &Delivery) term basically follows booking R/D term. But if booking R/D term includes M, then container R/D term has to be updated manually |
|  | Partial |  | Partial load indicator. When volume is smaller than 1, it will be flagged automatically. (User cannot un-flag it) |
|  | A/S |  | A(Advanced=Overland) or S(short ship=Short land) indicator when memo B/L flag appear. But user can update here. Based on this, shipment status will be shown on the Booking Master screen relevant to the Memo B/L as "ADV" for "A", 'SSH" for "S" |
|  | Special Cargo |  | Special Cargo Indicator. It will be ticked when the container is assigned in DG/BB/AK/RF cargo application |
|  |  |  | (DG-Dangerous, BB-Break Bulk, AK-Awkward, RF-Reefer Cargo), |
|  | Hanger |  | Hanger indicator. HG flag should be updated manually |
|  | SOC |  | SOC indicator. If the container is enrolled as SOC or SOC is declared on the Booking Master, SOC indicator will be automatically ticked |
|  | Origin(Yard) Event Date |  | Event place and Date where/when the latest Container Movement occurred relevant to the container No. together with movement status |
|  |  |  | > Status: OC |
|  |  |  | > Origin: Origin Yard (Yard where "OC" event occurred |
|  |  |  | > Event Date: Date of "OC"-Full Container Gate In |
|  | Cargo Receiving Date |  | Cargo Receiving date of each Container No. The first OC(Full Container Gate In) date becomes CRD. |
|  |  |  | (Note) When click "Container Confirmation", latest CRD among multiple Container No is applied to "CRD" for the Criteria of Freighting. |
|  | Special Cargo |  | Special Cargo Information Ex) Temp: - 10 ºC |
|  | Remark |  | Input Remark per container. |
| <Hereunder, result of action key appear above the each container Input item screen |  |  |  |
| Comparison |  |  | This shows the discrepancy the total quantity in overall between B/L Total and accumulated sum the each Container. For more details, click "Comparison detail" |
|  | Total Q'ty Comparison |  | -. Booking : Total Count in B/L Level |
|  |  |  | -. Container: Sum of each Container No ( Sum of individual container numbers ). |
|  |  |  | -. Discrepancy: If discrepancy is detected, different amount appears in Red color |
|  | Container Type/size |  | This shows the comparison result of Number of Container in container type/size level |
|  |  |  | > Type/Size : Container type size |
|  |  |  | > Booking : Booked Container Q'ty inputted in Booking Master |
|  |  |  | > Container: Input Result of Container Information |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="45/72" -->
<!-- PageBreak -->


### 25. 6. 10. 오후 1:42

about:blank


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
|  |  |  | > Registered : Input Result of Container Register |
|  |  |  | > Discrepancy :. When matched, Clear appear |


## 5) Button Explanation


| Category | Button Name | Explanation |
| --- | --- | --- |
| Each Container Information-Section |  |  |
| Grid1:Container detail- Input | [Add Row] | When "Booking B/L No" is selected as search key, it will be activated to make a input row of "Container No" |
|  | [Delete Row] | When "Booking B/L No" is selected as search key, it will be activated to make a input row of "Container No" |
|  | [Delete Container] | Delete the selected Container No and Initialize |
|  | [Export Excel] | Download B/L list appeared on the Grid with excel file |
|  | [Print] | Print container information on B/L. Below screen will pop-up |
|  | [Seal List] | Can review all of the container no and sealing status. |
|  | [Movement Trace] | Movement History will pop-up for easy cargo tracking purpose |
|  | [Not Updated Container] | When container number is sent from [MOV]-Movement system after container confirmation taken by Booking Staff, it will be displayed in below pop-up screen. If there is any data classified as "not updated container," this button will be colored in red for reminder to clarify. |
|  |  | When clicking "select," the selected container will be updated to container screen |
|  | [Update Receiving Date] | To reconcile the Cargo Receiving Date for Rating by Latest Gate In date when Gate in date are different. |
|  | [Part Load & Move] | Container copy and move function. Below screen is used to copy the part-load container No to the other Booking Nos or to move it under the "VL(Vessel Load) status to the other Booking No. |
|  |  | > "Copy" Process: (Part Load) |
|  |  | 1. Select the "Container No" and click [Part Load & Move] |
|  |  | 2. Click [Add Row] with "Copy". Then Target Booking No row is add "Copy" and click [Search]. The source booking number is displayed in the first row |
|  |  | 2. Type Target Bookings No with [Add Row] to be shared and input Package, Weight and Measurement. Then occupied ratio is automatically provided into the "To be" column in "Share Ratio" box (As default value of Proration criteria is Measurement. To adjust it, change "Prorate By" such as Weight or Package) |
|  |  | 3. Finally click "Apply". Then respective sharing ratio and details will be updated into the relevant Booking Nos respectively. |
|  |  | 'Move": |
|  |  | Move container to other booking. The volume of source booking will be fixed to 0, and the container volume of the other bookings should be assigned. If more than 2 bookings are assigned as target booking, then the container will be split into target bookings and partial indicator will be ticked |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="46/72" -->
<!-- PageBreak -->


## 25. 6. 10. 오후 1:42

about:blank


| Category | Button Name | Explanation |
| --- | --- | --- |
|  |  | Move "Container No" to upward or downward in the screen for B/L print purpose. |
|  |  | To select a target range, firstly place the pointer at the target container No and drag it down to the last one while the "Shift" key is pressed. Then all is selected. Then, click on the Descending (or Ascending) arrow button. To select multiple rows one by one and skip some rows, select certain rows while the "Ctrl" key is pressed |
|  | [Details per Cargo] | More detail comparison per container type/size and cargo type is shown |
|  | [Container Confirmation] | Perform final container confirmation. If this is taken, the container No flow in from "Container Movement" is blocked as well as not allowing to update data. |
|  | Or [Cancel Confirmation | Once "Container Confirmation" is taken, "Cancel Confirmation" is activated and vice versa. |


## 2.10. Special Cargo(DG/RF/AK/BB) Job List

1\) Navigation: Customer Service > Booking > Special Cargo(DG/RF/AK/BB) Job List


### 2) Screen Explanation

This is the screen that lists and shows the status of the special cargo in booking like (Requested,
Approved, Rejected, Pending).


### 3) Work Process

Input Booking Date (or On board Date, Requested Date, Vessel Voyage, Booking (B/L) No.) and any
other items as search key and "Search" then the booking list with special cargo will be shown in the grid
results. Check to select the Booking No. or Container No. then clicking "Detailed Information" to review
special cargo detail.


#### 4) Item Explanation


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
| Main | Booking date | :selected: √ | Booking Date(Max : 7days) |
|  | On board Date | :selected: √ | On board Date ( Max : 7days) |
|  | Requested Date | :selected: √ | Requested Date ( Max : 7days) |
|  | Vessel Voyage | :selected: √ | Working Vessel Voyage |
|  | Booking (B/L) No. | :selected: √ | Booking No./ B/L No. |
|  | Booking Office | :selected: √ | Booking Office Code ( Mandatory Item) |
|  | POL | :selected: √ | Working POL ( Mandatory Item ) |
|  | Requested Office | :selected: √ | Requested Office Code ( Mandatory Item ) |
|  | Booking Staff |  | The ID of booking staff who received booking. |
|  | Type |  | DOC format to be sent (Booking confirmation or Draft B/L) |
|  | POR/POL/POD/DEL |  | Route detail |
|  | B/L Office |  | Booking Office |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="47/72" -->
<!-- PageBreak -->


##### 25. 6. 10. 오후 1:42

about:blank


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
|  | Request Result |  | Request Result Code (D - Deleted, N - Rejected, P - Pending, R - Requested, Y - Approved, C - Cancel) |
|  | Shipper Code |  | Shipper Code on the "B/L Customer" screen |
|  | Shipper Name |  | Shipper Name on the "B/L Customer" screen |
|  | Non Approval & Container Match |  | Special cargo non approval and Container Match |
|  | Vessel Voyage |  | Vessel Voyage Code |
|  | POR , POL / POD , DEL |  | Route Detail |
|  | Booking No. |  | Booking No. |
|  | B/L No. |  | B/L No. |
|  | Booking Office |  | Booking Office Code |
|  | Requested by |  | Requested by (User ID) |
|  | Requested Office |  | Requested Office Code |
| Grid | [ ] Check |  | Check to select row seq. |
|  | No. |  | Seq. |
|  | Status |  | Special cargo status (Requested, Approved, Reject, Pending, Cancel ) |
|  | Cargo Type |  | Special Cargo type (Dangerous/ Reefer/Awkward/Break- Bulk/Stowage) |
|  | Vessel Voyage |  | Working Vessel Voyage code |
|  | POR , POL / POD , DEL |  | Route detail |
|  | Booking No. |  | Booking number. |
|  | B/L No. |  | Bill Of Lading number. |
|  | B/L Status |  | Booking Status (Waiting - Firm - Cancel) |
|  | Booking Office |  | Booking Office Code |
|  | Shipper |  | Indicates Shipper (Code) Name |
|  | Container Type/Size |  | Indicates Container Type/Size |
|  | Container No. |  | Indicates Container Number. |
|  | Booking Date |  | Booking Creation Date |
|  | On Board Date |  | On Board Date |
|  | Requested Date |  | Date of request |
|  | Requested Office |  | Requested Office Code (It should be same with login office) |
|  | Requested by |  | User ID of request staff |


###### 5) Button Explanation


| Category | Button Name | Explanation |
| --- | --- | --- |
| Main | Search | Search special cargo job list with search condition |
|  | Clear | Initialize search condition |
|  | Export Excel | Download special cargo job list in excel file |
|  | Detailed Information | Button to review special cargo detail |


## 2.11. Special Cargo

Overview

<!-- PageFooter="about:blank" -->
<!-- PageNumber="48/72" -->
<!-- PageBreak -->

<!-- PageHeader="25. 6. 10. 오후 1:42" -->
<!-- PageHeader="about:blank" -->

Special Cargo is classified into dangerous (Hazardous) cargo, reefer cargo and over-dimensional
awkward cargo or Break-Bulk cargo loaded onto the Containerized Vessel for which special attention
and approval is required by the Vessel Operation dep't prior to load within the given time frame as per
company rule.

Before approval of vessel operation department, booking status will be regarded as waiting booking
and it will be changed automatically to firm booking as soon as approval action is taken.

How to access application:

To create the Application, there are three options

\> Option1. Open individual Booking Master and select Special Cargo application button

\> Option2. Work with Booking with special cargo search option

\> Option3. Special Cargo (DG/RF/AK/BB) Job list


### 2.11.1. Dangerous (Request Special Cargo)

1\) Navigation: Customer Service > Booking > Request Special Cargo > Dangerous Tab


#### 2) Screen Explanation

This screen is to create, amend the special cargo information and request approval to SCC module. This
consists of four parts. First, upper two lines show the request Information about date, requester, status
and validation result. 2nd, 'Container Volume' grid shows the comparison between Booked Container
type/size and Quantity in the Booking Creation. 3rd, 'Container List' grid shows dangerous container
information. 4th, 'Cargo Detail for Container Seq.' section shows the detail of special cargo list for the
selected container sequence on 'Container List' grid.


#### 3) Work Process

Retrieve the "Booking Data" by giving "Booking No." as search option (When you create the Booking
Data with DG Booking, tick mark at the "Danger" and "Save")

Tick mark at the "Danger" and Assign DG container volume in "Rate Qty Detail" in the "Booking Master"
screen

Click "Danger" button in the" Booking Master" screen.

Select "Container No." or select container Type/Size if there's no container number. Usually, this request
should be done before empty container release time, therefore container sequence will take a tentative
role of physical container no. while request/approval. Later on, when the container number is fixed,

<!-- PageFooter="about:blank" -->
<!-- PageNumber="49/72" -->
<!-- PageBreak -->


##### 25. 6. 10. 오후 1:42

about:blank

make sure to fulfill the correct container number mapping to the container sequence. Otherwise, when
CLL (Container Load list) or Special Cargo Manifest is generated, container number or cargo detail does
not reflect on the list. (Note: Up to now, this process is commonly used for the other Reefer, Awkward
Cargo application as well.)

Input the details of cargo list per container: Select specific UN number and input all the needed
additional information such as weight, package quantity, type and so on. If multiple cargo to be stuffed
into one container, make a multiple record as many as cargo substance-UN number variance.

Request loading approval after inputting all of the needed information.

If you get the pre-check error result when you request it, you have to check 'Pre-checking Report' to
revise the information of the special cargo list you requested. Or, you can use 'Special Request" function
to pass pre-check validation without changing data.


#### 4) Item Explanation


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
| Top | Requested(Approved) By / Date |  | User ID of request staff and date of request or approve |
|  | Status |  | Request status |
|  |  |  | (Requested/Pre-check Error/Approved/Pending/Rejected/Cancel) For detail history, click 'Detail' button. |
|  | Validation Result |  | The reason of pre-checked error |
|  |  |  | (Carrier, Port, Packing, Segregation, Terminal, Vessel) |
|  | [Pre-checking Report] |  | By clicking this button, below screen will pop-up. This screen shows if the application may be accepted or not. If there's anything "to be prohibit" is detected, that dangerous cargo can be requested with mentioning the "Reason for Special Request" only through special request. Otherwise, "Special Request" button is not activated. |
| Container Volume Grid | Type/Size |  | It shows the list of container type/size set to dangerous cargo at the 'Booking Master'. |
|  | Booking |  | It shows the number of container by type/size at the 'Booking Master'. |
|  | Dangerous |  | It shows the number of container set to dangerous cargo by type/size at the 'Booking Master'. |
| Container List Grid | No. |  | The number sequence. |
|  | Slot. |  | The Slot Numbers of the containers are referenced from the Container Information screen. |
|  | Type/Size | :selected: √ | The Type/Size of each container. |
|  | Container No. | :selected: √ | The container number. |
|  | Volume | :selected: √ | The volume of each container. |
|  | Status |  | The request status of each container. |
|  | Related Special Cargo Seq. |  | The related special cargo sequence.(Awkward/Break Bulk/ Reefer) |
| Cargo Detail Section | Total cargo for Container |  | The number cargo of the container. |
|  | Container Seq. & No. |  | The sequence and number of selected container. |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="50/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

about:blank


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
|  | DG Ref. No. |  | The reference number of selected dangerous cargo. |
|  | Approval Ref. No. |  | The approval reference number of selected dangerous. |
|  | Status |  | The request status of each cargo (Requested/Pre-check Error/Approved/Pending/Rejected/Cancel) |
|  | UN No | √ :selected: | By clicking pop-up button or input UN NO, below "IMDG Code Inquiry by UN No." will pop-up. UN No. should be inputted through pop-up screen. |
|  | IMDG Class |  | IMDG class of selected UN No. |
|  | PSA Group |  | PSA group select column |
|  | Proper Shipping Name | √ :selected: | Proper shipping name(PSN) of selected UN No. and can be updated. |
|  | Technical Name |  | The technical name of selected UN No. and can be updated |
|  | Gross Weight | √ :selected: | Gross weight input column. If gross weight is smaller than net weight, the input will not be accepted |
|  | Net Weight | :selected: √ | Net weight input column. Net weight should not be larger than gross weight |
|  | Flash Point |  | If IMDG Class or Sub Risk Label is 3, flash point should be inputted |
|  | Package Qty/Type | √ :selected: | Mandatory item to input package/quantity. * Outer Package is mandatory item. |
|  | Packing Group |  | Packing group select column |
|  | Sub Label |  | Subsidiary Risk label of selected UN No. |
|  | [Restrict] |  | The "Restrict" screen that displays restrictions and regulation for inputted UN No. will pop-up |
|  | Cargo Status | :selected: √ | Select cargo status by selecting from drop down list(Gas/Liquid/Paste/Solid) in case of substance except class 2 -GAS, Class 3 -Liquid and Class4.1 Solid |
|  | Marine Pollutant | :selected: √ | Marine pollutant input column |
|  | Limited Qty | √ :selected: | Limited Qty status input column-Yes or No. *When Yes and Limited QTY is declared as Liter instead of kilograms, "Net Measure" in liter should be input. |
|  | Excepted Qty |  | Excepted Qty input column- Yes or No |
|  | Residue Last Contained |  | Check "Residue Last Contained or not" in case of the Empty Container |
|  | Segregation Group |  | Specify the Segregation group by manual. |
|  | Emergency Contact No. | :selected: √ | Emergency contact phone number. Mandatory item |
|  | Contact Person | :selected: √ | Emergency contact person |
|  | Certificate No. |  | In the countries where certificate number is mandatory item, input DG certificate number in this column |
|  | [Other Emergency Information] |  | By clicking this hypertext, below "Other Emergency Information" screen will spread. |
|  | [Detailed Package] |  | The section to input outer, intermediate and inner package will spread. * Outer Package is mandatory item. |
|  | Remark |  | The remark of dangerous cargo. |
|  | "Class 1 Only" tab | :selected: √ | If the IMDG class is 1, fill out the Consignee/Net Explosive Weight. |
|  | "Class 7 Only" tab | :selected: √ | If the IMDG class is 7, this tab should be filled out -Schedule, Activity and Transportation Index |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="51/72" -->
<!-- PageBreak -->

<!-- PageHeader="25. 6. 10. 오후 1:42" -->
<!-- PageHeader="about:blank" -->


## 5) Button Explanation


| Category | Button Name | Explanation |
| --- | --- | --- |
| Top | Go to Booking | The button for 'Booking Master' UI. |
|  | Search | The button for inquiry. |
|  | Route Detail | The button for 'Route Detail' UI. |
| Container Grid | Add Row | Add row to container grid. |
|  | Delete Row | Delete row to container grid. |
|  | Copy Container | Copy container sequence. |
| Cargo Section | Add Seq. | Add cargo sequence. |
|  | Delete Seq. | Delete cargo sequence. |
|  | Copy Seq. | When you want to copy current "Cargo Seq. DG Information" to the different Container No, click and select the target Container Number. |
|  | Cancel | Cancel request that has already been sent. |
| Bottom | Send Mail | Send DG information via e-mail. Below e-mail screen will pop-up |
|  | Print | Below screen will pop-up and the displayed format will be printed |
|  | Attach File | The button for attaching some files |
|  | Request | Request special cargo approval. All cargo sequence in a booking will be requested at once |
|  | Save | The button for saving |


### 2.11.2. Reefer (Request Special Cargo)

1\) Navigation: Customer Service > Booking > Request Special Cargo > Reefer Tab

2\) Screen Explanation

The screen to input reefer cargo detail and request loading approval


### 3) Work Process

Assign reefer container volume in volume detail screen

Select container or input container Type/Size if there's no container number.

Input reefer container settings and cargo information such as temperature, ventilation, package and
weight.

Request loading approval after inputting all of the needed information.

Make sure to map the correct container number to the container sequence when the container number
is fixed on S/I

4\) Item Explanation

<!-- PageFooter="about:blank" -->
<!-- PageNumber="52/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

about:blank


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
| Top | Requested(Approved) By / Date |  | User ID of request staff and date of request or approve |
|  | Status |  | Request status (Requested/Approved/Pending/Rejected/Cancel) For detail history, click 'Detail' button. |
|  | Total Package |  | The sum of inputted package in reefer cargo application. |
|  | Total Weight |  | The sum of inputted weight in reefer cargo application. |
| Container Volume Grid | Type/Size |  | It shows the list of container type/size set to reefer cargo at the ‘Booking Master'. |
|  | Booking |  | It shows the number of container by type/size at the Booking Master'. |
|  | Reefer |  | It shows the number of container set to reefer cargo by type/size at the Booking Master'. |
| Container List Grid | No. |  | The number sequence. |
|  | Slot. |  | The Slot Numbers of the containers are referenced from the Container Information screen. |
|  | Type/Size | √ :selected: | Container Type/Size. Type/Size should be inputted although container number is not assigned. |
|  | Container No. | √ :selected: | The container numbers inputted in container screen will be displayed in drop down list. (If no container when apply at the booking time, it may be blank. But when container No is obtained, make sure to map it to the container seq. no) |
|  | Volume | √ :selected: | Volume of assigned container The sum of volume should not be larger than Reefer Quantity. |
|  | Danger | :unselected: O | if the container is also declared as Dangerous cargo. |
|  | Gen set |  | Generator set usage mark |
|  | Volt |  | The voltage of generator |
|  | Status |  | Approval status per each container |
| Cargo Detail Section | Container Seq. & No. |  | The sequence and number of selected container. |
|  | Approval Ref. No. |  | The approval reference number of selected dangerous. |
|  | Status |  | The request status of each cargo (Requested/Approved/Pending/Rejected/Cancel) |
|  | Commodity | √ :selected: | Reefer commodity. Basically, system will pull out booking commodity but you can edit it to meet exact commodity name |
|  | Temperature | :selected: √ | Reefer container temperature setting. |
|  | Nature | :selected: √ | The nature of cargo. Nature can be selected in drop down list (Frozen, Chilled, Fresh) |
|  | Sensitive Cargo |  | The Sensitive Cargo. Select it form the Drop down list. (BLOOD PLASMA, ICE CREAM, USDA) |
|  | Ventilation | :selected: √ | Ventilation setting. Only one of '% Open' and CBM/Hour can be selected. |
|  | Control Atmosphere |  | If CA container is required, input control condition |
|  | Modified Control Atmosphere | :selected: √ | Modified Atmosphere container indicator |
|  | Humidity Control |  | Humidity Control container indicator |
|  | Drain |  | The indicator to mark drain status (CLOSE, N/A, OPEN) |
|  | Humidity |  | Humidity percentage input column |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="53/72" -->
<!-- PageBreak -->


## 25. 6. 10. 오후 1:42

<!-- PageHeader="about:blank" -->


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
|  | Gross Weight | √ :selected: | Gross weight input column. It should not be smaller than net weight |
|  | Net Weight |  | Net weight input column. It should not be larger than gross weight |
|  | Package |  | Package input column. Both package number and unit have to be inputted |
|  | Remark | O :unselected: | The remark information of the each cargo |


## 5) Button Explanation


| Category | Button Name | Explanation |
| --- | --- | --- |
| Top | Go to Booking | The button for 'Booking Master' UI. |
|  | Search | The button for inquiry. |
|  | Route Detail | The button for 'Route Detail' UI. |
| Container Grid | Add Row | Add row to container grid. |
|  | Delete Row | Delete row to container grid. |
|  | Copy Container | Copy container sequence. |
| Cargo Section | Cancel | Cancel request that has already been sent. |
| Bottom | Request | Request special cargo approval. All cargo sequence in a booking will be requested at once |
|  | Save | The button for saving |


### 2.11.3. Awkward (Request Special Cargo)

1\) Navigation: Customer Service > Booking > Request Special Cargo > Awkward Tab

2\) Screen Explanation

The screen to input awkward cargo detail and request loading approval


### 3) Work Process

Assign awkward container volume in "Rate Q'ty detail screen on Booking Master.

Select container or input container Type/Size if there's no container number.

Input awkward container settings and cargo information such as dimension or corner post status.
Request loading approval after inputting all of the needed information.

Make sure to map the correct container number to the container sequence when the container number
is fixed on S/I


#### 4) Item Explanation

<!-- PageFooter="about:blank" -->
<!-- PageNumber="54/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

about:blank


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
| Top | Requested(Approved) By / Date |  | User ID of request staff and date of request or approve |
|  | Status |  | Request status (Requested/Approved/Pending/Rejected/Cancel) For detail history, click 'Detail' button. |
|  | Total Package |  | The sum of inputted package in awkward cargo application. |
|  | Total Weight |  | The sum of inputted weight in awkward cargo application. |
| Container Volume Grid | Type/Size |  | It shows the list of container type/size set to reefer cargo at the ‘Booking Master'. |
|  | Booking |  | It shows the number of container by type/size at the ‘Booking Master'. |
|  | Awkward |  | It shows the number of container set to awkward cargo by type/size at the 'Booking Master'. |
| Container List Grid | No. |  | The number sequence. |
|  | Slot. |  | The Slot Numbers of the containers are referenced from the Container Information screen. |
|  | Type/Size | √ :selected: | Container Type/Size. Type/Size should be inputted although container number is not assigned. |
|  | Container No. | √ :selected: | The container numbers inputted in container screen will be displayed in drop down list. (If no container when apply at the booking time, it may be blank. But when container No is obtained, make sure to map it to the container seq. no) |
|  | Volume | √ :selected: | Volume of assigned container The sum of volume should not be larger than Awkward Quantity. |
|  | Danger | :unselected: O | if the container is also declared as Dangerous cargo. |
|  | Status |  | Approval status per each container |
| Cargo Detail Section | Container Seq. & No. |  | The sequence and number of selected container. |
|  | Approval Ref. No. |  | The approval reference number of selected dangerous. |
|  | Status |  | The request status of each cargo (Requested/Approved/Pending/Rejected/Cancel) |
|  | Commodity | √ :selected: | AK cargo commodity basically follows booking commodity. This commodity can be changed if needed to show exact commodity name |
|  | Gross Weight | :selected: √ | Gross weight of cargo. It should not be smaller than net weight |
|  | Net Weight | √ :selected: | Net weight of cargo. It should not be larger than gross weight |
|  | Receiving/Delivery term | :selected: √ | Awkward cargo container Receive/Delivery term. AK term will basically follow booking term and AK term remains inactivated. But if booking term has M, then AK term will be activated |
|  | Package | :selected: √ | Input The number of packages to be stuffed in the Container |
|  | Corner Post Status |  | Corner post status of container in case of extendable container. |
|  | Over Height after Extension |  | "Over Height after Extension" can be updated manually. |
|  | Post Lock Pin |  | :selected: A type container: post lock pin will be set as "Y" and can be updated manually. |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="55/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

<!-- PageHeader="about:blank" -->


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
|  |  |  | F type container: post lock pin will be empty and cannot be updated manually. |
|  | Gravity Center |  | Input gravity center information if needed |
|  | Total Dimension | √ :selected: | Input cargo dimension in total base (Total Length/Width/Height -Unit: CM) |
|  | Over Dimension |  | When total dimension is input, Over-dimension will be automatically calculated. |
|  | Void Space |  | Void space will be automatically calculated according to over dimension based on the Container Spec on the "Criteria Info" pop up. Also, It can be updated manually. |
|  |  |  | If void slot occurs, insert the Void slot in the Booking Master with using virtual dead space equipment of "Q2 or Q4 type/size for statistics as well as accurate. |
|  | Stowage Request |  | Input stowage request if needed |
|  | Remark |  | Type Remark of awkward cargo if necessary .. |
|  | Under deck top (check box) |  | When Under Deck Top stowage is requested, tick mark |


## 5) Button Explanation


| Category | Button Name | Explanation |
| --- | --- | --- |
| Top | Go to Booking | The button for 'Booking Master' UI. |
|  | Search | The button for inquiry. |
|  | Terminal Information | The button for 'Terminal Information' UI. |
| Container Grid | Add Row | Add row to container grid. |
|  | Delete Row | Delete row to container grid. |
|  | Copy Container | Copy container sequence. |
| Cargo Section | Criteria Info. | The screen that shows over dimension calculation criteria will pop-up. And it is used as criteria of Void slot calculation. |
|  | Detailed Package | The screen to input cargo details will pop-up. If there is any detail inputted, button will be colored in blue |
|  | Cancel | Cancel request that has already been sent. |
| Bottom | Attach File | The button for attaching some files |
|  | Request | Request special cargo approval. All cargo sequence in a booking will be requested at once |
|  | Save | The button for saving |


### 2.11.4. Break Bulk (Request Special Cargo)

1\) Navigation: Customer Service > Booking > Request Special Cargo > Break Bulk Tab

2\) Screen Explanation

The screen to input break bulk cargo detail and request loading approval


#### 3) Work Process

Assign break bulk container volume in volume detail screen

Select container or input container Type/Size if there's no container number

<!-- PageFooter="about:blank" -->
<!-- PageNumber="56/72" -->
<!-- PageBreak -->


## 25. 6. 10. 오후 1:42

about:blank
Input awkward container settings and cargo information such as dimension or corner post status.

Request loading approval after inputting all of the needed information.


### 4) Item Explanation


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
| Top | Requested(Approved) By / Date |  | User ID of request staff and date of request or approve |
|  | Status |  | Request status (Requested/Approved/Pending/Rejected/Cancel) For detail history, click 'Detail' button. |
| Cargo Lines Summary Grid | No. |  | Seq. |
|  | Piece |  | Piece count |
|  | Pack |  | Piece code |
|  | Commodity Group |  | Commodity Group Code/Name |
|  | G.Weight(KG) |  | Gross Weight |
|  | CBM |  | Measure |
|  | Length |  | Length (cm) |
|  | Width |  | Width (cm) |
|  | Height |  | Height (cm) |
|  | Price Type |  | Price Type |
|  | Status |  | Status of break bulk (Requested, Approved, Rejected, Pending, Cancel) |
| Cargo Detail Section | Seq No. |  | Seq. |
|  | Piece Count | √ :selected: | Input piece count of the item as package. |
|  | Commodity | √ :selected: | Item classification code by clicking on the search button icon to |
|  |  |  | open pop-up |
|  | HS Code |  | Item classification code by clicking on the search button icon to open pop-up |
|  | Commodity Group | :selected: √ | Item classification code by clicking on the search button icon to open pop-up |
|  | Operational Package | :selected: √ | Input Operational Package Code or clicking on the search button icon to open pop-up |
|  | Exact Commodity | :selected: √ | Exact Commodity description |
|  | Gross Weight | :selected: √ | Input Gross Weight |
|  | Receiving /Delivery Term |  | Cargo Receive & Delivery term (e.g. Y/Y- CY/CY ... ) |
|  | Price Type |  | Select price type for each sequence break bulk (R - Revenue TON, W - Gross Weight, M - Measure, L - Lump sum, P - PIECE) |
|  | Dimension |  | Input cargo dimension information. (Length/Width/Height) (cm) |
|  | [ ] Per piece |  | Measure(CBM) will be calculated per Piece Count |
|  | Measure |  | Measure in each sequence break bulk |
|  | Dangerous Cargo. |  |  |
|  | UN No. |  | By clicking pop-up button or input UN NO, below "IMDG Code Inquiry by UN No." will pop-up. UN No. should be inputted through pop-up screen. If not, other information |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="57/72" -->
<!-- PageBreak -->


## 25. 6. 10. 오후 1:42

about:blank


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
|  |  |  | such as IMDG Class and proper shipping name will not be updated. |
|  | Class |  | IMDG class of selected UN No. |
|  | Proper Shipping Name |  | Proper shipping name(PSN) of selected UN No. and can be updated |
|  | DG Gross Weight |  | Gross weight of Dangerous cargo . If gross weight is smaller than net weight, the input will not be accepted |
|  | DG NET Weight |  | Net weight of Dangerous cargo. Net weight should not be larger than gross weight |
|  | Flash Point |  | If IMDG Class or Sub Risk Label is 3, flash point should be inputted |
|  | Emergency Contact |  | Emergency contact phone number |
|  | Outer Package |  | Special request input column |
|  | Remark |  | Input Remark for Dangerous cargo. |
|  | Remark for Bulk Cargo |  | The remark of Break Bulk cargo. |


## 5) Button Explanation


| Category | Button Name | Explanation |
| --- | --- | --- |
| Top | Go to Booking | The button for 'Booking Master' UI. |
|  | Search | The button for inquiry. |
|  | Terminal Information | The button for 'Terminal Information' UI. |
| Cargo Lines Summary Grid | [ ] Show Cancel | Show the sequences canceled. |
|  | Add Row | Add row to container grid. |
|  | Delete Row | Delete row to container grid. |
|  | Cancel | Cancel request that has already been sent. |
| Bottom | Copy to Mark&Goods | Copy data in the Cargo Lines Detail area from this screen to Marks & Goods Description screen. |
|  | Attach File | The button for attaching some files |
|  | Request | Request special cargo approval. All cargo sequence in a booking will be requested at once |
|  | Save | The button for saving |


### 2.11.5. Stowage (Request Special Cargo)

1\) Navigation: Customer Service > Booking > Request Special Cargo > Stowage Tab


### 2) Screen Explanation

The screen to retrieve stowage information and request approval


### 3) Work Process

Select stowage type settings and remark information.

Request approval after inputting all of the needed information.


#### 4) Item Explanation

<!-- PageFooter="about:blank" -->
<!-- PageNumber="58/72" -->
<!-- PageBreak -->


## 25. 6. 10. 오후 1:42

<!-- PageHeader="about:blank" -->


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
| Top | Requested(Approved) By / Date |  | User ID of request staff and date of request or approve |
|  | Status |  | Request status |
|  |  |  | (Requested/Approved/Pending/Rejected/Cancel) For detail history, click 'Detail' button. |
| Container Volume Grid | Type/Size |  | It shows the list of container type/size set to break bulk cargo at the 'Booking Master'. |
|  | Booking |  | It shows the number of container by type/size at the 'Booking Master'. |
|  | Package/Weight/Measure/Description |  | Cargo information for Package/Weight/Measure/Description |
| Stowage Type Grid | Type |  | The Stowage type code. |
|  | Detail |  | The description of each stowage type. |
| Else | Remark |  | The remark of stowage detail. |


## 5) Button Explanation


| Category | Button Name | Explanation |
| --- | --- | --- |
| Top | Go to Booking | The button for 'Booking Master' UI. |
|  | Search | The button for inquiry. |
| Container Grid | Delete | Delete stowage type information |
| Bottom | Request | Request special cargo approval. All cargo sequence in a booking will be requested at once |
|  | Cancel | Cancel request that has already been sent. |
|  | Save | The button for saving |


### 2.12. DG Suspicious Booking Monitor / verify

1\) Navigation: Customer Service > Booking > DG Suspicious Booking Monitor / verify


#### 2) Screen Explanation

This screen is to display suspicious bookings which are needed to be verified for DG check. When
creating bookings with description of goods detected by "Danger Keyword Creation", the booking
information is displayed on this screen. Also, as user can see specific menu on "Source", the suspicious
keyword is written on the menu (ex. Marks & Goods Description).


#### 3) Work Process

Input "Created On" as duration to check suspicious keyword detection.
Other input boxes are optional.

<!-- PageFooter="about:blank" -->
<!-- PageNumber="59/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

about:blank


##### 4) Item Explanation


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
| Main | <Search key to retrieve the data> |  |  |
|  | Created On | √ :selected: | The time suspicious keyword detected |
|  | Vessel Voyage | √ :selected: | Vessel Voyage Code |
|  | POL |  | Port of Loading |
|  | POD |  | Port of Discharging |
|  | Verify |  | Verify (ALL / Y / N) |
|  | Source |  | Suspicious Keyword detected menu (M&D or H/BL) |
| Grid | <Displayed Items after search> |  |  |
|  | No. |  | Seq |
|  | Verify |  | Y = no more warning message for suspicious keyword for the booking |
|  |  |  | N = Keep showing warning message for suspicious keyword for the booking |
|  | B/L No. |  | B/L Number |
|  | B/L Status |  | BKG Status (F - Firm / W - Waiting / X - Cancelled) |
|  | C/N |  | Correction Notice description. |
|  | DG Supply |  | Y = Applied for DG application / N = Not applied for DG application yet |
|  | DG Suspicious Words(Three Word) |  | Detected word as suspicious |
|  | Source |  | Suspicious Keyword detected menu (M&D or H/BL) |
|  | DG Keyword |  | Full letters of DG Keyword |
|  | Vessel Voyage |  | Vessel Voyage Code |
|  | POL |  | Port of Loading |
|  | POD |  | Port of Discharging |
|  | Verified On |  | The time of "Verify -> Y" saved |
|  | Verified By |  | The person verified |
|  | Created On |  | The time suspicious keyword detected |
|  | Created By |  | The person created the suspicious keyword in the menus |


## 5) Button Explanation


| Category | Button Name | Explanation |
| --- | --- | --- |
| Main | Search | Search booking list with search condition |
|  | Clear | Initialize search condition |
|  | Export Excel | Download Vessel Voyage list in excel file |


## 2.13. Booking Close for Bay Plan

1\) Navigation: Customer Service > Booking >Booking Close for Bay Plan


### 2) Screen Explanation

This is made for internal communication between booking office and Vessel Planner exchanging the
"Close Booking" at the Booking Office for the vessel planner to start the "Bay plan" job. Once "Close
Booking" is taken by Booking office by office, this can allow for vessel planner to check the all of
Booking Office Closing status related to the Vessel Voyage/POL before start to Bay plan in the vessel
planner view

<!-- PageFooter="about:blank" -->
<!-- PageNumber="60/72" -->
<!-- PageBreak -->


#### 25. 6. 10. 오후 1:42

about:blank

Also, after booking closing, it give the alert message to the Booking Staff when they try to create
additional booking or to update major information which may impact the making a Bay Plan


#### 3) Work Process

Input Vessel Voyage, POL and "Search"

Select the row for Booking Closing and Click "Close Booking", Then all of Booking related to this Vessel
Voyage/POL/Booking Office will be the target as " Close Booking"

When you re-open it, click "Re-Open Booking" button.


##### 4) Item Explanation


| Category | Item Name | Mandatory Explanation |  |
| --- | --- | --- | --- |
| Main | <Search key to retrieve the data> |  |  |
|  | Vessel Voyage | √ :selected: | Vessel Voyage (Mandatory Item) |
|  | POL | √ :selected: | Vessel POL (Mandatory Item) |
|  | POL Yard |  | Vessel POL Facility |
|  | POD |  | Vessel POD |
|  | Office |  | Booking Office (It should be same with login office. Other office user can't do booking close action) |
|  | Status |  | Open + Re-Open / Close / Open / Close / Re-Open |
|  | <Displayed Items after search> |  |  |
|  | [ ] Check |  | Check to select row sequence. |
|  | No. |  | Seq. |
|  | Vessel Voyage |  | Vessel Voyage |
|  | POL |  | Vessel POL |
|  | POL Yard |  | POL Facility Code |
|  | POL Call Seq. |  | POL Calling Sequence |
|  | POD |  | Vessel POD |
|  | Booking Office |  | Booking Office Code |
|  | Status |  | Booking Status(Open/Closed) |
|  | Office |  | Data update user office |
|  | Update ID |  | Data update user id |
|  | Update Date |  | Data update Date |


###### 5) Button Explanation


| Category | Button Name | Explanation |
| --- | --- | --- |
| Main | Search | Search booking list with search condition |
|  | Clear | Initialize search condition |
|  | Export Excel | Download Vessel Voyage list in excel file |
|  | Close Booking | Close Booking for specific VVD / POL / Booking office (Booking office should be same with login user office) |
|  | Re-open Booking | Re-open closed booking VVD / POL / Booking office (Booking office should be same with login user office) |


## 2.14. Transmit Booking Fax/Email/EDI

<!-- PageFooter="about:blank" -->
<!-- PageNumber="61/72" -->
<!-- PageBreak -->


## 25. 6. 10. 오후 1:42

about:blank

This is a function to convert booking data saved after booking data creation into formats of Booking
Receipt Notice and Empty Container Release Order in order to allow users to batch search and send via
fax, email, or EDI multiple data by using period information such as a VVD or Booking Creation Date as
well as an individual booking number assigned to each customer, port terminal, or container depot.


### 2.14.1. Booking Receipt Notice (Fax/Email)

1\) Navigation: Customer Service > Booking >Transmit Booking Fax/Email/EDI > Booking Receipt Notice
(Fax/Email)


#### 2) Screen Explanation

This is the screen where user can send booking confirmation to customers.


##### 3) Work Process

"Search" Bookings to be sent to customer after key in various "Search" condition

If you edit the Email, or Fax No, input directly at the E-mail, Fax column.

When you want to batch update "Fax and Email" address for the multiple Booking Nos. with same Fax.
(or Email) No, Select the target Booking No. click "Edit Fax &Email" and update it.

When you update "Remark", click "Remark" column in the list.
Finally, Click "Send Fax" or "Send Email" button to send it.


###### 4) Item Explanation

Category

Item Name

Mandatory Explanation

Main

<Search key to retrieve Booking No list> - Type search key and "Search".

As basic key, anyone among "Booking Date" or "Vessel Voyage" or "Booking B/L No" is required


| Date & Vessel/Voyage | :selected: √ | Booking Date (Max: 31 days). |
| --- | --- | --- |
|  |  | <Merged Condition> |
|  |  | It is mandated together with anyone among "POR, POL, Booking Office, Booking Staff, Sales Office or Sales Rep) |
| BKG No. | √ :selected: | Booking Number |
| Vessel Voyage | :selected: √ | Input VVD and other item |
|  |  | <Merged Condition> |
|  |  | It is mandated together with anyone among "POR, POL, Booking Office, Booking Staff, Sales Office or Sales Rep) |
| Booking Office | √ :selected: | Booking Office together with "Booking Date or VVD" |
| Booking Staff | :selected: √ | Booking Staff. It is mandated with "Booking Creation Date or VVD" |
| Booking Status |  | Booking Status. Even if you select "all", canceled and advanced booking are not included |
| Booking Kinds |  | Booking received channel (i.e. OFF, WEB, EDI, GTN, etc.) |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="62/72" -->
<!-- PageBreak -->


## 25. 6. 10. 오후 1:42

about:blank


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
|  | POR |  | Booking Place of Receipt |
|  | POL |  | Working Place of Loading& Yard where the given VVD calls |
|  | POD |  | Working Place of Discharging& Yard where the given VVD calls |
|  | DEL |  | Booking Delivery |
|  | Fax Status |  | Sending Status (No Send, Sending, Success, Failed) |
|  | Customer |  | Select Customer Type and type 2 Country Digit + 6 Number for filtering |
|  | Loading Office/Sales Rep. |  | Load Office of Booking main/Sales. Rep code |
|  | E-Mail Status |  | Sending Status (No Send, Sending, Success, Failed) |
| Grid | <Displayed Items after searching key is given> |  |  |
|  | [ ] Check |  | Check to select row sequence. |
|  | No. |  | Seq. |
|  | Booking No. B/L No. |  | By double-clicking, Booking main screen pops up |
|  | Status |  | Booking Status (F-Firm, W-Waiting, S-Master B/L, X-Cancel) |
|  | Need BRN Resend |  | Whether BRN should be resent or not |
|  | Plus |  | If you click "+" icon, new row for selected booking is added and you can input other e-mail number to send more than 2 e-mails for one booking at the same time |
|  | Via |  | Booking Receipt Channel (OFF-Booking created by manual type, WEB from E-Commerce, EDI. INT,GTN, etc.) |
|  | Office |  | Booking Office Code |
|  | Shipper |  | Shipper Code and Name |
|  | Fax Number |  | Fax No of BKG contact of booking main screen. |
|  | Fax Result |  | Fax Send Result ("M" button for detail POPUP screen) |
|  | Fax Send Date |  | Fax send date |
|  | Email Address |  | Check E-mail No of BKG contact of booking main screen. |
|  | Email Result |  | Email Send Result ("M" button for detail POPUP screen) |
|  | Email Send Date |  | Email send date |
|  | Port CCT |  | Port Cut-Off (Terminal) of "Cut Off Time" pops up of Booking main screen |
|  |  |  | Original / Current / Manual (Not used for PIL) |
|  | DOC CCT |  | Document Cut Off time |
|  | Remark |  | This information displays on "P.S" part of Booking Receipt Notice |
|  | Trunk Vessel/Voyage |  | Trunk VVD |
|  | POR/POL/POD/DEL |  | Route information |
|  | Booking Staff |  | Booking staff who received booking. |
|  | Contact PIC |  | Contact of booking contact of Booking main screen |


## 5) Button Explanation


| Category | Button Name | Explanation |
| --- | --- | --- |
| Main | [Search] | Search booking list with search condition |
|  | [Clear] | Initialize search condition and result |
|  | [Export Excel] | Download booking list in excel file |
|  | [Preview] | Open preview pop-up |
|  | [Edit CCT] | This is group editing of port CCT for selected bookings |
|  | [Send Fax] | Send Fax |
|  | [Send Email] | Send Email |
|  | [Edit Fax/Email] | This is group editing of fax or email for selected bookings |
|  | [Assign Agent Email] | This is for booking by Chinese booking agents. If you select booking and click this button, Email is changed with booking agent Email |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="63/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

about:blank


### 2.14.2. Booking & S/I Receipt Notice (EDI)

1\) Navigation: Customer Service > Booking >Transmit Booking Fax/Email/EDI > Booking & S/I Receipt
Notice (EDI)


### 2) Screen Explanation

This is the screen where users can Booking confirmation via EDI to customers.


### 3) Work Process

"Search" Bookings to be sent to customer after key in various "Search" condition
Before transmit EDI, EDI for customers should be set in advance.

When you want to batch send EDI to multiple customers, select them and click "Send to Customer"
button.


#### 4) Item Explanation


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
| Main | Date & Vessel/Voyage | √ :selected: | Booking Date(Max : 7days) |
|  | Vessel Voyage |  | Working Vessel Voyage |
|  | Booking B/L No. |  | Booking No./ B/L No. |
|  | [ ] SAMSUNG |  | Used for SAMSUNG partners. |
|  | Booking Office |  | Booking Office Code |
|  | Booking Staff |  | The ID of booking staff who received booking. |
|  | Type |  | DOC format to be sent (Booking confirmation or Draft B/L) |
|  | POR/POL/POD/DEL |  | Route detail |
|  | B/L Office |  | Booking Office |
|  | Customer |  | Customer code/Name |
|  | Loading Office/Sales Rep. |  | Sales rep and loading office |
|  | EDI Send Status |  | Send status (Sent - Unsent) |
|  | EDI Receiver |  | EDI receiver code |
|  | Contract No. |  | Contract No. or Agreement No. |
| Grid | [ ] Check |  | Check to select row seq. |
|  | No. |  | Seq. |
|  | Booking(B/L) No |  | Booking Number |
|  | Booking Information(Via/Office) |  | Method which booking is created, such as OFF(manual creation), INTTRA or GTNEXUS |
|  | Customer |  | Customer Name |
|  | Group EDI ID |  | In case of EDI, Group ID |
|  | EDI Reference |  | EDI Reference. It is used in EDI customer |
|  | EDI Receiver |  | EDI receiver code |
|  | Receiver Name |  | Name of receiver code |
|  | Vessel Voyage |  | Vessel Voyage |
|  | POR/POL/POD/DEL |  | Route detail |
|  | Sent Time |  | Time that EDI has been transmitted. |
|  | Sent ID |  | Staff who click "Send to" button |
|  | Sent Status |  | Result of sending EDI |
|  | Ack. |  | Ack message |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="64/72" -->
<!-- PageBreak -->


## 25. 6. 10. 오후 1:42

about:blank


### 5) Button Explanation


| Category | Button Name | Explanation |
| --- | --- | --- |
| Main | Search | Search booking list with search condition |
|  | Clear | Initialize search condition |
|  | Export Excel | Download Booking No list in excel file |
|  | Send to Customer | Button to send selected booking EDI to Customer |
|  | Send to Terminal | Button to send selected booking EDI to Terminal |


#### 2.14.3. Transmit Booking EDI to Terminal

1\) Navigation: Customer Service > Booking >Transmit Booking Fax/Email/EDI > Transmit Booking EDI to
Terminal

2\) Screen Explanation (It can be changed on way to EDI Setup)

This is the screen to send Booking Information to terminal via EDI in Non-US regions


### 3) Work Process

Search Bookings to be sent to terminal

Edit EDI Message if needed
Click "Transmit" button


#### 4) Item Explanation


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
| Main | Date & Vessel/Voyage | :selected: √ | Booking Data (Max: 7 days) |
|  | Vessel/Voyage |  | Working Vessel Voyage |
|  | Booking B/L No. |  | Booking No./ B/L No. |
|  | Booking Office |  | Booking Office Code |
|  | Booking Staff |  | The ID of booking staff who received booking. |
|  | POL |  | Working Place of Loading |
|  | Booking Status |  | Booking Status (ALL/Firm/Waiting/Advanced/Cancel) |
|  | EDI Sent Status |  | Unsent, Sent |
|  | Lane |  | Lane of VVD |
| Grid | [ ] Check |  | Check to select row seq. |
|  | No. |  | Seq. |
|  | Booking No |  | By double-clicking, booking main screen pops up |
|  | Booking Office |  | Booking Office Code |
|  | Date |  | Booking Date |
|  | B/L No. |  | B/L Number |
|  | B/L No. Type |  | B/L Split status |
|  | Status |  | Booking Status (ALL/Firm/Waiting/Advanced/Cancel) |
|  | Full/Empty |  | Full / Empty (Cargo Type) |
|  | Flex Height |  | Indicates Flex Height Cargo Y/N |
|  | Special Cargo |  | Special Cargo Information |
|  | Trunk Vessel/Voyage |  | Trunk VVD Code |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="65/72" -->
<!-- PageBreak -->


## 25. 6. 10. 오후 1:42

about:blank


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
|  | ETB |  | Estimated Berth Time |
|  | Lane |  | Lane Code |
|  | POL Port |  | POL Port Code |
|  | POL Yard |  | POL Facility Code |
|  | EDI Receiver |  | EDI Receiver |
|  | EDI Send Date |  | EDI Send Date |
|  | EDI Send ID |  | EDI Send ID |


## 5) Button Explanation


| Category | Button Name | Explanation |
| --- | --- | --- |
| Main | Search | Search booking list with search condition |
|  | Clear | Initialize search condition |
|  | Export Excel | Download Booking No list in excel file |
|  | Transmit | This is to send EDI for selected booking |


### 2.14.4. Empty Container Release Order

1\) Navigation: Customer Service > Booking >Transmit Booking Fax/Email/EDI > Empty Container Release
Order


### 2) Screen Explanation

This is the screen to send empty container release order to pick up yard


### 3) Work Process

Retrieve Bookings to be sent to customer

Edit Email or Fax No if need

Edit Remark if need
Click "Fax", "E-mail" or "EDI" button


### 4) Item Explanation


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
| Main | Date | :selected: √ | Booking Date or Empty Pick Up Date (Max 31 days) |
|  | Vessel/Voyage |  | Working Vessel Voyage |
|  | Booking B/L No. |  | Booking No./ B/L No. |
|  | Type |  | The Type Selection (Simple, Detail, Detail(USA)) |
|  | POR/POL/POD |  | Route |
|  | Pick-up CY |  | Pick-up CY |
|  | Return CY |  | Return CY |
|  | Booking Office |  | Booking Office Code |
|  | Booking Staff |  | The ID of booking staff who received booking. |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="66/72" -->
<!-- PageBreak -->


### 25. 6. 10. 오후 1:42

<!-- PageHeader="about:blank" -->


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
|  | Pick Up CY Control Office |  | Empty Pick Up CY Control Office of booking main |
|  | EQ Manager Confirm |  | Manually updated by EQ manager if Empty container release order sent |
| Grid | [ ] Check |  | Check to select row seq. |
|  | No. |  | Seq. |
|  | Booking No |  | By double-clicking, booking main screen pops up |
|  | R/D Term |  | Destination transportation methods defined |
|  | Container Volume |  | The amount of container for WHF collection in the port for each bound by VVD |
|  | Flex Height |  | Indicates Flex Height Cargo Y/N |
|  | POR/POL |  | Route |
|  | Pick-up CY |  | Displays pick-up CY for booking |
|  | CY Name |  | Name for CY code |
|  | Pick-up Date |  | Display pick-up date |
|  | EDI Target Y/N |  | Y/N |
|  | BRN Sent |  | Status of Booking Receipt Notice(Booking confirmation) sent |
|  | Vessel Voyage |  | Vessel code |
|  | Vessel Name |  | Vessel Name of the VVD |
|  | EQ Confirm |  | Y / N |
|  | Fax No. |  | Representative Fax No of Pick-Up CY |
|  | Email |  | Representative E-mail No of Pick-Up CY |
|  | Shipper |  | Shipper Code and Name |
|  | Commodity |  | Item classification code for making and rating the loading list for customs submission ( Commodity Code ) |
|  | Commodity Detail |  | Commodity Name |
|  | Vendor Remark |  | Input 'Remarks" associated with Vendor such as Depot, Trucking Co etc. This will be reflected on the "Empty Container Release order Notice" |
|  | Remark(Temporary) |  | Remark |


## 5) Button Explanation


| Category | Button Name | Explanation |
| --- | --- | --- |
| Main | Search | Search booking list with search condition |
|  | Clear | Initialize search condition |
|  | Sum by Yard | EQ Demand Trend by Pick Up CY Pop up |
|  | Edit P/Up CY & Remark | Update Empty Release Order Information Pop up |
|  |  | - Pick-up CY |
|  |  | - Return CY |
|  |  | - Pick-up Date |
|  |  | - Vendor Remark |
|  |  | - Remark(Temporary Use) |
|  | Export Excel | Download Booking No list in excel file |
|  | Print | print Empty Release Order of selected booking list |
|  | Send EDI | This is to Send EDI for selected booking |
|  | Send Fax | This is to Send Fax for selected booking |
|  | Send Email | This is to Send Email for selected booking |
|  | Edit Email | This is group editing of email for selected bookings |
|  | Update Fax & Email | This is button for Fax & Email Update |
|  | EQ Manager Confirm | Confirm Y/N by EQ Manager authority |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="67/72" -->
<!-- PageBreak -->


## 25. 6. 10. 오후 1:42

<!-- PageHeader="about:blank" -->


## 2.15. Booking Status Change

1\) Navigation: Customer Service > Booking > Booking Status Change


### 2) Screen Explanation

The screen is used for actual loading office to change the Booking Status which has been
automatically made as Waiting for the Cross-Trade booking or Non-approved special cargo booking or
intentional Waiting for operation purpose by office.

It can be handled by batch job process for the selected booking Nos. with ease. Also, this enable us to
change the Booking status compulsorily to "Firm" for emergent case when necessary to proceed next
step such as B/L issue but not-approved from the special cargo handling center in spite of loaded on the
vessel or due to unexpected irregularity


### 3) Work Process

Input VVD (or Booking Creation period) and any other items as search key and "Search"
Select the Booking No to change "status" by clicking "Waiting to Firm" or "Firm to Waiting"

In case of emergency, you may use "Compulsory Firm" very strictly. In that case, status can be changed
to "Firm", although special cargo is not approved from the controller part in due course.


#### 4) Item Explanation


| CategoryItem | Name | Mandatory | Explanation |
| --- | --- | --- | --- |
| Main | <Search key to retrieve the data> |  |  |
|  | Vessel Voyage | :selected: √ | Input VVD with other anyone item. This is mandatory item unless there's data in Booking No. column. |
|  | Date | :selected: √ | Input booking creation period. It should be merged with at least any other condition |
|  | Booking B/L No. | :selected: √ | Input Booking B/L number. If this is inputted, you don't need to input other conditions |
|  | POL |  | Input Place of Loading. The bookings of same POL will be listed |
|  | POD |  | Input Place of Discharging. The bookings of same POD will be listed |
|  | Booking Status |  | Booking status selection (W-Waiting, F-Firm, All, Cancel) |
|  | Booking Office |  | Input booking office. The bookings of same booking office will be listed |
|  | Special Cargo type |  | Special Cargo type (Dangerous/Awkward/Break- Bulk/Reefer/PC/Special Stowage) : Multi Selectable |
|  | Loading Office |  | Input Sales Office. Code |
|  | Sales Rep. |  | Input Sales Rep. Code |
|  | Shipper |  | Input shipper code and name. The bookings of same shipper will be listed |
|  | Forwarder |  | Input forwarder code and name. The bookings of same forwarder will be listed |
| Grid | <Scope of Data Display and Reason of Waiting Booking> |  |  |
|  | Data Display Scope |  | When the search option is given, retrieval data range is limited to the portion relevant to 1st loading Port (POL) under jurisdiction of log-in office for the security control about the Cross-Trade Booking Status Change. |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="68/72" -->
<!-- PageBreak -->


##### 25. 6. 10. 오후 1:42

<!-- PageHeader="about:blank" -->


| CategoryItem | Name | Mandatory | Explanation |
| --- | --- | --- | --- |
|  |  |  | The reason is why any office can take a booking for the other loading port with "Waiting" Booking status but the status change to "Firm" should be allowed by the loading port office user only. |
|  | Which situation make booking as Waiting Status? |  | Booking Status is changed to "Waiting" under following situation. |
|  |  |  | 1) When Special Cargo (DG/AK/BB) application is not approved |
|  |  |  | 2) Cross-Trade Booking Creation and Booking Copy |
|  |  |  | 3) Status Change of "Firm to Waiting" by user's intention |
|  |  |  | 4) When Booking Master Data is updated by the other office user not directly related to the POL (Target: POR/POL/POD/DEL, TSP, Receive & Delivery Term, VVD and Booking Container Type/Size and Quantity) |
| Result | <Displayed Items after search> |  |  |
|  | [ ] Check |  | Check to select row seq. |
|  | No. |  | Seq. |
|  | Status |  | Booking status selection (F-Firm, W-Waiting) |
|  | Booking No. |  | Booking No. |
|  | Booking Office |  | Booking Office Code |
|  | DPC |  | DPC(Document Process Closing) status |
|  | Waiting Reason |  | SP(Special Cargo-Non Approval), CB(Cross Booking), VS(Vessel Space Problem), ES(Equipment Shortage), CM(Commodity), OT(Others) |
|  | Special Cargo |  | Indicates Special Cargo type(DG: Dangerous/RF: Reefer/AK: Awkward/BB: Break-Bulk) |
|  | CM(USD) |  | Estimated Contribution Margin(USD) |
|  | Trunk Vessel/Voyage |  | Trunk Vessel/Voyage Code |
|  |  |  | VVD- Trunk VVD, T.POL- POL of Trunk VVD , Shipper, Forwarder, Commodity, Booking Quantity break-down by TEU/TEU ,Weight, POD |
|  | Trunk POL |  | Trunk POL Code of Trunk Vessel/Voyage |
|  | Trunk POD |  | Trunk POD Code of Trunk Vessel/Voyage |
|  | Roll Over Times |  | Roll over times if it happened. |
|  | Sales Rep. |  | Sales Rep. Code |
|  | Shipper /Class |  | Shipper's Name and Class Code (Value Base Segmentation Class Code) |
|  | Consignee/Class |  | Consignee's Name and Class Code (Value Base Segmentation Class Code) |
|  | Forwarder/ Class |  | Forwarder's Name and Class Code (Value Base Segmentation Class Code) |
|  | Rep. commodity |  | Rep. Commodity Code and Description |
|  | FEU |  | 40Ft Type Container Unit |
|  | TEU |  | 20Ft Type Container Unit |
|  | Ton |  | Kilogram Tonnage (1,000KGS) |


##### 5) Button Explanation


| Category | Button Name | Explanation |
| --- | --- | --- |
| Main | Search | Search booking list with search condition |
|  | Clear | Initialize search condition and result |
|  | Compulsory Firm (Waiting -> Firm) | Changes booking status to F compulsorily. This will change booking status without checking any condition |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="69/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

about:blank


| Category | Button Name | Explanation |
| --- | --- | --- |
|  | Waiting -> Firm | Change booking status to F. But if it is before special cargo approval or it is a Cross-Trade Booking, booking status will not be changed. |
|  | Firm -> Waiting | Change booking status to W. But if it is a Cross-Trade Booking, booking status will not be changed and after container VL, booking status will not be changed. |
|  | Cancel -> Firm | Reinstate the Cancelled booking status to Firm. But if it is a Cross-Trade Booking, booking status will not be allowed by the user not belonging to the POR. |


## 2.16. VGM Dashboard

1\) Navigation: Customer Service > Booking >VGM Dashboard


### 2) Screen Explanation

This is the screen to search VGM Dashboard which came from various EDI channel and to fix it as
declared value to the related Booking No and Container No by the Documentation staff.

Also, through this user can go the CLL (Container Load List)


### 3) Work Process

Input Vessel/Voyage Code and POL or Booking Number (or B/L Number) as mandatory item to search
VGM data.

If you reduce the data search range, Input additional conditions like Booking Office, Booking Staff and
give "Detail Search" condition

Click [Search] button to search booking list.

Click [VGM Upload] button to upload excel for VGM.

Click [Export Excel] button to download booking list.
Click [Print] button to open pop-up (Container Loading/Discharging List)

Click [Send Email] button to send Email.

Click [Go to CLL] button to open pop-up (Container Loading/Discharging List)

Click [EDI(Manual)] button to open pop-up (VGM EDI)

Click [Close VGM] button to fix the declared VGM after selected Booking No/Container Nos. Once it is
taken, further VGM data which shall flow in this VGM dashboard later on does not replace the
manifested VGM on the Container Load List.

Click [Activated VGM] button to activate closed VGM.

<!-- PageFooter="about:blank" -->
<!-- PageNumber="70/72" -->
<!-- PageBreak -->


## 25. 6. 10. 오후 1:42

about:blank


### 4) Item Explanation


| Category | Item Name | Mandatory | Explanation |
| --- | --- | --- | --- |
| Search | Vessel Voyage | √ :selected: | Input Vessel Voyage Code |
|  | POL | √ :selected: | Input POL(Port of Loading) |
|  | Booking/B/L No. | √ :selected: | Input Booking / B/L Number. |
|  | Booking Office |  | Booking Office |
|  | Booking Staff |  | The ID of booking staff who received booking |
|  | POD |  | Input POD(Port of Discharging) |
|  | Booking/On board period |  | Input Booking Creation or On board period. |
|  | VGM Option |  | Select Received / Not Received |
|  | VGM |  | Select E-COM / EDI |
|  | Receiving/ Delivery Term |  | Select CY / Door / CFS / Tackle / Free In / Mixed |
|  | Customer |  | Input Customer ID |
|  | Missing signatory |  | Select Missing signatory Y/N |
|  | Late Update |  | Select Late Update Y/N |
| Result | [ ] Check |  | Check to select row seq. |
|  | No. |  | Seq. |
|  | Booking No. |  | Indicates Booking No |
|  | B/L No. |  | Indicates B/L Number. |
|  | Office |  | Booking Office |
|  | Trunk Vessel Voyage |  | Indicates Trunk Vessel Voyage Code |
|  | POL |  | Indicates POL Code |
|  | POD |  | Indicates POD Code |
|  | ETD of 1st Port |  | Indicates ETD(Estimated Time of Departure) of 1st port |
|  | VGM Cut off |  | Indicates Cut Off Time VGM |
|  | Shipper |  | Indicates Shipper Code |
|  | [ ] Check |  | To select. |
|  | Container No. |  | Indicates Container Number. |
|  | Type Size |  | Indicates Container Type/Size |
|  | Declared VGM -VGM |  | Indicates Declared VGM |
|  | Unit |  | Indicates Declared VGM Unit |
|  | User ID |  | Indicates Declared User ID. |
|  | Update |  | Indicates Declared Update Date. |
|  | Latest VGM -Via |  | Indicates Latest External VGM Request Code. |
|  | VGM |  | Indicates Latest VGM. |
|  | Unit |  | Indicates Latest VGM Unit. |
|  | User ID |  | Indicates Latest User ID. |
|  | Update |  | Indicates Latest Update Date. |
|  | e-Signature |  | Indicates e-signature Y/N. |
|  | Close VGM - Close |  | Indicates Close VGM Y/N |
|  | User ID |  | Indicates Close User ID. |
|  | Date |  | Indicates Close Date. |


## 5) Button Explanation


| Category | Button Name | Explanation |
| --- | --- | --- |
| Main | Search | Search booking list with search condition |
|  | Clear | Initialize Search Conditions. |
|  | Export Excel | Downloads the Result Grid Data in excel file |
|  | Print | Open Pop-up "Container Loading/Discharging List" to print. |
|  | Send Email | Open Pop-up "Container Loading/Discharging List" to send Email. |
|  | History | Open Pop-up "VGM History" to search VGM history. |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="71/72" -->
<!-- PageBreak -->

25\. 6\. 10\. 오후 1:42

about:blank


| Category | Button Name | Explanation |
| --- | --- | --- |
|  | Go to CLL | Open Pop-up "Container Loading/Discharging List" to Send EDI. |
|  | EDI(Manual) | Open Pop-up to select the "VGM EDI" partner to Send EDI (Manual). |
|  | Close VGM | Close Selected Container No -VGM to the manifested CLL. To cross=check the data relationship, refer to the 'VGM" field on the "Container No" screen |
|  | Activated VGM | Activate closed VGM |


<!-- PageFooter="about:blank" -->
<!-- PageNumber="72/72" -->
