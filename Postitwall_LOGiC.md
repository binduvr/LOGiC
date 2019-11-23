# Postitwall LOGiC

## Energy awareness tool

### General

### To do

### Possible improvements
* Coupling with other tooling
  * Coupling with the microgrid assessment tool would enalble the user to make a very detailled profile of a community without having to understand demand profiling
* Input annual demand by user, for further scaling of the annual profile
  * scale back annual profile after season trends are applied
  * generally think about improving profile forging based on one input day;
    * Week
    * Season
*
## Microgrid assessment tool

### General
In general it is a good idea to rebuild the MAT. The tool is quite a contraption at the moment.
Requirements should at least include:
#### Requirements
* parallel computing (either in cbc or multiple terminals)
* Status updates from the python terminal to the website
*

### To do (current version)

### Possible improvements (current version)

#### Technical
* Wind turbine autoselection (wind batch, power curve, capex)

#### Economical
* Make more explicit results and statements about earning back the investment
* compare to a BAU scenario (grid?)
* Add lifetime to estimated investment cost
*


#### Outputs
* show OPEX (report, webpage)
*

## Web page
* different screensizes possible
* make tool use more appealing; sugestions Ewout:
  * M.b.t. pagina http://offgridtestcenter.nl/dhes/ Lijkt me goed als mensen op het 1e scherm meteen kunnen zien waar ze naartoe moeten als ze iets van de tooling willen gebruiken. Deze zin maakt in ieder geval nog niet helemaal helder wat de bedoeling is – terwijl je hier mensen wilt verleiden om gebruik te maken van deze mooie tool:
    * Design your community to discover what is in for your energy usage.
    * Online tool to create and determine the energy consumption of a region, building, or a space. A valuable tool for installers, project developers and people who want meaningful insights about energy consumption and saving opportunities.
* "Requests assessment" suggest a purchase/some more required action. Reword this button
* Reconsider season placement; winter = Q1?
* Clarify more about the advanced setting; IMHO (Marien) opinion this really needs a rework: some relevant remarks by Ewout (information bullet that expands when moued over/clicked on)
  * fill out categorised forms (on tabs) with standard valuees based on a wind and solar guess and invite the user to edit the fields or leave the standards
  * remodel page (Marien: architecture)
* results page: Can the non-used compenents be removed/greyed out in the timelapse?
