Memory,bset,pc,n,z,v,c,sign_extend,Stump=type("Memory",(object,),dict(__init__=(lambda self,size:[setattr(self,"size",size),setattr(self,"memory",[0]*size)][-1]),__getitem__=(lambda self,a:self.memory[a]),__setitem__=(lambda self,a,v:self.memory.__setitem__(a,v)))),(lambda i,b:(i&b)==b),7,8,9,10,11,(lambda n,b:((-1 if bset(n,1<<(b-1)) else 0)<<b)|n),type("Stump",(object,),dict(__init__=(lambda self,memory:[setattr(self,"memory",memory),setattr(self,"_regs",[0]*(8 + 4)),setattr(self,"cc_en",False)][0]),__getitem__=(lambda self,r:sign_extend(self._regs[r],16) if r!=0 else 0),__setitem__=(lambda self,r,v:getattr(self,"_regs").__setitem__(r,v&0xFFFF if r<=7 or self.cc_en else self._regs[r])),geta=(lambda self,instr:(lambda val,carry:[val,self.__setitem__(n,bset(val,0x8000)),self.__setitem__(z,val==0),self.__setitem__(v,0),self.__setitem__(c,carry)][0])(*(((self[(instr>>5)&0b111]),0) if (self.instr_type==2 or (instr&0b11==0)) else (lambda carry:(lambda _val:(_val|(([val>>14,carry,self[c]][(instr&0b11)-1])<<15),carry))(((self[(instr>>5)&0b111])>>1)&0x7FFF))((self[(instr>>5)&0b111])&0x1)))),getb=(lambda self,instr:self[(instr>>2)&0b111] if self.instr_type==1 else sign_extend(instr&0b11111,5)),addr=(lambda self,i:sign_extend(self.geta(i)+self.getb(i),16)),add=(lambda s,i,cin,inv=False:((lambda a,b:(lambda val:[s.__setitem__((i>>8)&0b111,val&0xFFFF),s.__setitem__(n,bset(val,0x8000)),s.__setitem__(z,val==0),s.__setitem__(c,((val&0xFFFF)<(a&0xFFFF))^inv),s.__setitem__(v,((a<0)and(b<0)and(val>=0))or((a>=0)and(b>=0)and(val<0)))])(sign_extend((a+b+cin)&0xFFFF,16)))(s.geta(i),(s.getb(i)^(-1*inv))))),step=(lambda self:(lambda instr:[setattr(self,"instr_type",3 if bset(instr,0xF000) else bset(instr,0x1000)+1),setattr(self,"cc_en",bset(instr,0x800) and not(bset(instr,0xC000))),[self.memory.__setitem__(self.addr(instr),self[(instr>>8)&0b111]) if instr&0xE800==0xC800 else (self.__setitem__((instr>>8)&0b111,self.memory[self.addr(instr)]) if instr&0xE800==0xC000 else (self.add(instr,bset(instr,0x2000)*self[c]) if instr&0xC000==0x0 else (self.add(instr,(1+(bset(instr,0x2000)*self[c]))%2,True) if instr&0xC000==0x4000 else None))),self.__setitem__((instr>>8)&0b111,self.geta(instr)&self.getb(instr)) if instr&0xE000==0x8000 else (self.__setitem__((instr>>8)&0b111,self.geta(instr)|self.getb(instr)) if instr&0xE000==0xA000 else None)] if self.instr_type in (1,2) else (self.__setitem__(pc,self[pc]+sign_extend(instr&0xFF,8)) if bool(eval(reduce(lambda p,r:p.replace(*r),[(x,"self[%s]"%x) for x in "nzvc"]+[("!","not "),("."," and "),("+"," or ")],"False|c+z|c|z|v|n|!n.v+n.!v|(!n.v+n.!v)+z".split("|")[((instr&0xF00)>>8)>>1])))==bset((instr&0xF00)>>8,0b1) else None)][0])([self.memory[self[pc]],self.__setitem__(pc,self[pc]+1)][0]))))