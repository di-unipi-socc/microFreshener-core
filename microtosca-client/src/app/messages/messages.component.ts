import { Component, OnInit } from '@angular/core';
import { MessageService } from '../message.service';

@Component({
  selector: 'app-messages',
  templateUrl: './messages.component.html',
  styleUrls: ['./messages.component.css']
})
export class MessagesComponent implements OnInit {

  constructor(public messageService: MessageService) { } 
  // public: because nit is bounded to a templarte
  // look into messages.components.html
  // *ngIf="messageService.messages.length

  ngOnInit() {
  }

}
