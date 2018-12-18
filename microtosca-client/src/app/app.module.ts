import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';

import { FormsModule } from '@angular/forms'; // <-- NgModel lives here

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeroesComponent } from './heroes/heroes.component';
import { HeroDetailComponent } from './hero-detail/hero-detail.component';
import { MessagesComponent } from './messages/messages.component';
import { MenuComponent } from './menu/menu.component';

// Import primeNG modules
import {AccordionModule} from 'primeng/accordion';
import { DiagramEditorComponent } from './diagram-editor/diagram-editor.component';

//import d3js component
import { D3Service, D3_DIRECTIVES} from './d3';
import { GraphComponent } from './visuals/graph/graph.component';
import { SHARED_VISUALS } from './visuals/shared';
import { MenuEditComponent } from './menu-edit/menu-edit.component';

@NgModule({
  declarations: [
    AppComponent,
    HeroesComponent,
    HeroDetailComponent,
    MessagesComponent,
    MenuComponent,
    DiagramEditorComponent,
    GraphComponent,
    ...SHARED_VISUALS,
    ...D3_DIRECTIVES,
    MenuEditComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    FormsModule,
    AccordionModule
  ],
  providers: [ D3Service],
  bootstrap: [AppComponent]
})
export class AppModule { }
