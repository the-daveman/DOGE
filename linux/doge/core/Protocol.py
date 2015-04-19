from ctypes import *
from protocol_ctypes import *

libprotocol = CDLL("./doge/core/libprotocol.so")

def form_packet(type=RAW_PACKET, srcID=1, dstID=1, cmd=CMD_READ_REG, addr=0, data=0):
   #TODO generalize error check for type and cmd to list valid names instead of the numeric range
   if(type not in range(1, MAX_PACKET_TYPE)): raise Exception("The packet type, {0}, must be in the range [1, 8]".format(type))
   if(srcID not in range(0, 2**16)): raise Exception("The source ID, {0}, must be in the range [0, 65535]".format(srcID))
   if(dstID not in range(0, 2**16)): raise Exception("The destination ID, {0}, must be in the range [0, 65535]".format(dstID))
   if(cmd not in range(1, 6)): raise Exception("The command, {0}, must be in the range [1, 5]".format(cmd))
   if(addr not in range(0, 2**8)): raise Exception("The address, {0}, must be in the range [0, 255]".format(addr))
   if(data not in range(0, 2**8)): raise Exception("The data, {0}, must be in the range [0, 255]".format(data))

   appPkt = appPacket()
   rawPkt = rawPacket()
   attr = packetAttr()

   libprotocol.application_form_packet(byref(rawPkt.data), byref(attr), cmd, addr, data)
   libprotocol.link_layer_form_packet(byref(rawPkt), byref(attr), type, srcID, dstID)
   
#   print("\n\tPacket: \n\t[{0}], size = {1}, data = {2}".format(print_structure(rawPkt.hdr), rawPkt.size, list(i for i in rawPkt.data)))

   toSend = packetToList(rawPkt)
   return toSend
 
def receive_packet(stream, registers):
   raise Exception("Protocol.receive_packet has been deprecated.")
   # Returns response array
   rxBuffer = 0
   byteNum = 0
   checksum = 0
   execute = 0
   remainder = []
   response = ""


   cmd = 0
   size = 0
   addr = 0
   data = 0
   
   stream.reverse()
   while(len(stream)>0):
      rxBuffer = stream.pop()

      #convert just in case
      if(type(rxBuffer) is str):
         rxBuffer = ord(rxBuffer)

      byteNum = byteNum + 1
      checksum = checksum + rxBuffer

      if(byteNum == 1):
         cmd = rxBuffer
      elif(byteNum == 2):
         size = rxBuffer
      else:
         if( (size + 3) > byteNum): #not at checksum if true
            remainder.append(rxBuffer)
         else: #at checksum if true
            if(checksum%256 == 0):
               execute = 1
            else:
               response = form_packet(NACK, 0, BAD_CHECKSUM)
               execute = 0
               byteNum = 0
               checksum = 0
               remainder = []
               return response

      if(execute == 1):
         if(cmd == READ_REG):
            addr = remainder[0]
            print("Got read_reg. Addr = " + str(addr) + "\n")
            response = form_packet(ACK, addr, registers[addr])
         elif(cmd == WRITE_REG):
            addr = remainder[0]
            data = remainder[1]
            print("Got write_reg. Addr = " + str(addr) + ", Data = " + str(data) + "\n")
            registers[addr] = data
            response = form_packet(ACK, addr, registers[addr])
         elif(cmd == ACK):
            addr = remainder[0]
            data = remainder[1]
            print("Got ack. Addr = " + str(addr) + ", Data = " + str(data) + "\n")
         elif(cmd == NACK):
            addr = remainder[0]
            data = remainder[1]
            print("Got nack. Addr = " + str(addr) + ", Data = " + str(data) + "\n")
         elif(cmd == NOP):
            print("Got nop\n")
         else:
            print("Unknown command: " + str(cmd) + "\n")
            response = form_packet(NACK, 0, BAD_COMMAND)
         execute = 0
         byteNum = 0
         checksum = 0
         remainder = []
         return response

