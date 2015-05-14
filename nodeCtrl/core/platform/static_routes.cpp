#include "static_routes.h"

extern dogePacket txPacket;
extern appPacket* txAppPacket;
extern packetAttr txAttr;

extern dogePacket rxPacket;
extern appPacket* rxAppPacket;
extern packetAttr rxAttr;

uint8_t static_route_mm_handler(uint8_t rw, uint8_t addr, uint8_t* data, uint8_t mask)
{
   switch(addr)
   {
      case(NRF24_NODE_11_OFFSET):
         print_string("SENDING TO NODE 11", NEWLINE);
         break;
      case(NRF24_NODE_12_OFFSET):
         print_string("SENDING TO NODE 12", NEWLINE);
         break;
      case(NRF24_NODE_13_OFFSET):
         print_string("SENDING TO NODE 13", NEWLINE);
         break;
      case(NRF24_NODE_14_OFFSET):
         print_string("SENDING TO NODE 14", NEWLINE);
         break;
      case(NRF24_NODE_15_OFFSET):
         print_string("SENDING TO NODE 15", NEWLINE);
         break;
      case(NRF24_NODE_16_OFFSET):
         print_string("SENDING TO NODE 16", NEWLINE);
         break;
      case(NRF24_NODE_17_OFFSET):
         print_string("SENDING TO NODE 17", NEWLINE);
         break;
      case(NRF24_NODE_18_OFFSET):
         print_string("SENDING TO NODE 18", NEWLINE);
         break;
   }
   application_form_packet(txAppPacket, &txAttr, CMD_READ_REG, NRF24_DEFAULT_APP_ADDRESS, *data, NULL);
   link_layer_form_packet(&txPacket, &txAttr, RAW_PACKET, MY_NODE_ID, addr, MY_NODE_ID, addr);
   nrf24_send(0, (uint8_t*)(&txPacket), MAX_DATA_LENGTH);
   while(nrf24_isSending());
   return 0;
}
