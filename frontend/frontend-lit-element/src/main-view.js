import { LitElement, html, css } from 'lit-element'; 
import '@polymer/paper-dropdown-menu/paper-dropdown-menu.js';
import '@polymer/paper-item/paper-item.js';
import '@polymer/paper-listbox/paper-listbox.js';
import '@vaadin/vaadin-select';
import '@vaadin/vaadin-date-picker';
import '@vaadin/vaadin-time-picker';
import '@vaadin/vaadin-combo-box';

class MainView extends LitElement { 
  constructor(){
    super()
    this.park = ""
    this.rides = [""]
    this.magicKingdomRides = ["Space Mountain", "Big Thunder Mountain"]
    this.animalKingdomRides = ["Flights of Passage", "Everest"]
    this.epcotRides = ["Soarin", "Test Track"]
    this.hollywoodStudioRides = ["Rock N Rollercoaster", "Tower of Terror"]
    this.comboDisabled = true;
    this.waitTimeGotten = false;
    this.buttonDisabled = true;
    this.selectedRide = "";
    this.currentWaitTime = "";

  }

  static get properties(){
    return{
      park: {type:String},
      rides: {type:Array},
      time: {type:String},
      magicKingdomRides: {type:Array},
      comboDisabled: {type:Boolean},
      selectedRide: {type:String},
      waitTimeGotten: {type:Boolean},
      currentWaitTime: {type:String},
      buttonDisabled: {type:Boolean}
    }
  }

  static get styles(){
    return [
      css`
      h2{
        padding-top: 1em;
        text-align: center;
        font-size: 2em;
        color: black;
        max-width: 13em;
        margin: auto;
      }

      h1{
        color: green;
        font-size: 8em;
        margin-top: .25em;
        margin-bottom: 0em;
        text-align: center
      }

      h3{
        font-size: 2em;
        text-align: center
      }

      .main-container{
        
        background: rgba(255, 255, 255, .5);
        width: 75em;
        margin: auto;
        height: 40em;
        margin-top: 0em;
        border-radius: 1.5em;
      }

      .div-left{
        float: left;
        width: 37.5em;
      }

      .div-right{
        font-family: var(--lumo-font-family);
        float: left;
        width: 37.5em;
        height: 35em;
      }

      .div-right-opaque{
        background: rgba(255, 255, 255, 1);
        width: 30em;
        margin-left: .5em;
        margin-top: 6em;
        height: 27em;
        border-radius: 1.5em;
        border: 1px solid grey;
        box-shadow: 5px 5px 5px grey;
      }

      .wait-time-not-gotten{
        margin: auto;
        padding-top: 1.25em;
        text-align: center;
        font-size: 3em;
      }

      .date-picker{
        padding: 5em 0 0 10em;
      }

      .time-picker{
        padding: 1em 0 0 10em;
      }

      .park-select{
        padding: 1em 0 0 10em;
      }

      .ride-select{
        padding: 1em 0 0 10em;
      }

      .wait-time-button{
        clear: both;
        display: flex;
        margin: auto;
        margin-top: 5em;
      }

      #wait-time-button{
        color: white;
        border: 1px solid grey;
        border-radius: 9px;
        box-shadow: 2.5px 2.5px 2.5px grey;
      }
      `
    ] 
  }
  render() {
    console.log("Render")
    console.log(this.rides)
    return html`
      <div class="main-container" >

        <div class="div-left">
          <p class="main-text" ></p>

          <div class="date-picker" >
            <vaadin-date-picker id="date-picker" theme="date-picker-theme" label="Date"  placeholder="Pick a date" @change="${this.updateDate}">
            </vaadin-date-picker>
          </div>

          <div class="time-picker" >
            <vaadin-time-picker  id="time-picker" theme="time-picker-theme" label="Time" @value-changed="${this.updateTime}"></vaadin-time-picker>
          </div>

          <div class="park-select" >
            <vaadin-select id="park-picker" theme="park-picker-theme" label="Parks" @value-changed="${this.updatePark}">
              <template>
                <vaadin-list-box>
                  <vaadin-item>Animal Kingdom</vaadin-item>
                  <vaadin-item>Epcot</vaadin-item>
                  <vaadin-item>Hollywood Studios</vaadin-item>
                  <vaadin-item>Magic Kingdom</vaadin-item>
                </vaadin-list-box>
              </template>
            </vaadin-select>
          </div>

          <div class="ride-select">
                ${this.comboDisabled ? (
                  html`<vaadin-combo-box theme="disabled-ride-picker-theme" label="Rides" disabled items="${JSON.stringify(this.rides)}"></vaadin-combo-box>`
                ): (html`<vaadin-combo-box id="ride-picker"  theme="ride-picker-theme" label="Rides" items="${JSON.stringify(this.rides)}" @value-changed="${this.updateRide}"></vaadin-combo-box>`)}
          </div>
        </div>

        <div class="div-right">
          <div class="div-right-opaque">
          ${!this.waitTimeGotten ? (
            html`<div class="wait-time-not-gotten">Please Select a Date, Time, Park and Wait Time and hit the button to get a predicted wait time</div>`
          ): (html`<h2>Expected Wait Time for ${this.selectedRide}</h2>
              <h1>${this.currentWaitTime}</h1>
              <h3>Minutes</h3>`)}
          </div>  
        </div>

        <div class="wait-time-button">
        ${this.buttonDisabled ? (
        html`<vaadin-button disabled id="wait-time-button" theme="disabled-button-theme" style="margin:auto" @click=${this.calculateWaitTimes}>Calculate Wait Times</vaadin-button>`
        ): (html`<vaadin-button id="wait-time-button" theme="primary" style="margin:auto" @click=${this.calculateWaitTimes}>Calculate Wait Times</vaadin-button>`)}
        </div>

      </div>
    `
  }

  updatePark(e){
    this.park=e.detail.value;
    switch(this.park){
      case "":
        this.rides=[""];
        break;
      case "Magic Kingdom": 
        this.rides=this.magicKingdomRides;
        console.log(this.rides);
        break;
      case "Animal Kingdom":
        this.rides=this.animalKingdomRides;
        break;
      case "Epcot":
        this.rides=this.epcotRides;
        break;
      case "Hollywood Studios":
        this.rides=this.hollywoodStudioRides;
        break;
      default: console.log("How?!?");
    }
    this.rides.sort;
    this.comboDisabled=false;
    console.log("Updating")
    this.requestUpdate();
  }

  getRides(){
    return html
  }

  updateTime(e){
    console.log(e.detail.value)
  }

  updateDate(e){
    let datePicker = this.shadowRoot.getElementById("date-picker").value 
  }

  updateRide(e){
    this.buttonDisabled = false;
    this.requestUpdate();
  }

  async sendGetRequest(){
    await fetch('https://jsonplaceholder.typicode.com/todos/1')
    .then(
      response => response.json()
    )
    .then(
      res => console.log(res)
    )
  }

  async sendPostRequest(date, time, park, ride){
    let body = {
      date: date,
      time: time,
      park: park,
      ride: ride
    }
    await fetch('https://jsonplaceholder.typicode.com/posts', {
      method: 'POST',
      headers:{
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    })
    .then(
      response => response.json()
    )
    .then(
      res => console.log(res)
    )
  }

  calculateWaitTimes(){
    let date = this.shadowRoot.getElementById("date-picker").value;
    let time = this.shadowRoot.getElementById("time-picker").value;
    let park = this.shadowRoot.getElementById("park-picker").value;
    let ride = this.shadowRoot.getElementById("ride-picker").value;
    this.selectedRide = ride;
    this.currentWaitTime = "300";
    this.waitTimeGotten = true;
    this.requestUpdate();
  }

}

customElements.define('main-view', MainView);