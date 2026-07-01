<!-- MemNet snap: R&S oscilloscope SCPI conventions.
Wire format per skill: memnet-format. Anchor: TSK_rs_scpi.
Load via: memnet MCP query_warm(anchor="TSK_rs_scpi", depth=2)
Fallback: read this file directly. Ignore this comment and the fenced
wrapper below — the @TAG rows inside are the canonical wire. -->

```memnet
@TSK: TSK_rs_scpi|R&S oscilloscope SCPI conventions|active|persistent

# ---------- Core rules ----------

@RUL: R01|MUST|write long-form SCPI in source (CHANnel1:WAVeform1:DATA:VALues?)|high|persistent
@RUL: R02|MUST|channel data queries go through CHANnel<n>:WAVeform<w> subtree|high|persistent
@RUL: R03|MUSTNOT|use AUToscale in scripted automation|high|persistent
@RUL: R04|MUST|Single-shot = TRIGger:MODE NORMal + RUNsingle (no SING mode value)|high|persistent
@RUL: R05|MUST|drain SYSTem:ERRor:NEXT? until +0,"No error" after each critical block|high|persistent
@RUL: R06|MUST|use *OPC? (query) unless SRQ armed; *OPC alone is event only|med|persistent
@RUL: R07|MUST|set FORMat:DATA REAL,32 + FORMat:BORDer LSBFirst before every binary read|high|persistent
@RUL: R08|MUST|parse DATA:HEADer? for time axis; never hard-code|high|persistent
@RUL: R09|MUST|handle vals_per_sample=2 as [min,max] pairs (peak/envelope)|high|persistent
@RUL: R10|MUSTNOT|send *RST at connect; only on explicit user reset|high|persistent

# ---------- Canonical capture sequence (ordered @CLM chain) ----------

@CLM: CAP_S1|type=pipe|*CLS + SYSTem:DISPlay:UPDate ON|persistent
@CLM: CAP_S2|type=pipe|*IDN? and *OPT? into run metadata|persistent
@CLM: CAP_S3|type=pipe|check_error_queue() (drain SYST:ERR?)|persistent
@CLM: CAP_S4|type=pipe|STOP; CHANnel<n>:STATe + CHANnel<n>:SCALe per channel|persistent
@CLM: CAP_S5|type=pipe|ACQuire:TYPE SAMPle; ACQuire:INTerpolation SINX|persistent
@CLM: CAP_S6|type=pipe|ACQuire:POINts:MODE MANual; ACQuire:POINts N|persistent
@CLM: CAP_S7|type=pipe|ACQuire:SRATe:MODE MANual; ACQuire:SRATe fs|persistent
@CLM: CAP_S8|type=pipe|TIMebase:SCALe s; TIMebase:REFerence 0..100 (percent); TIMebase:HORizontal:POSition|persistent
@CLM: CAP_S9|type=pipe|TRIGger:MODE NORMal; TRIGger:EVENt1:SOURce CHANnel<n>; TYPE EDGE; LEVel<n>; EDGE:SLOPe|persistent
@CLM: CAP_S10|type=pipe|*OPC? then check_error_queue()|persistent
@CLM: CAP_S11|type=pipe|FORMat:DATA REAL,32; FORMat:BORDer LSBFirst; EXPort:WAVeform:INCXvalues OFF|persistent
@CLM: CAP_S12|type=pipe|RUNsingle; *OPC?; check_error_queue()|persistent
@CLM: CAP_S13|type=pipe|per ch: CHANnel<n>:WAVeform1:DATA:HEADer? then DATA:VALues?; check_error_queue()|persistent

@EDG: CAP_S1|next|CAP_S2
@EDG: CAP_S2|next|CAP_S3
@EDG: CAP_S3|next|CAP_S4
@EDG: CAP_S4|next|CAP_S5
@EDG: CAP_S5|next|CAP_S6
@EDG: CAP_S6|next|CAP_S7
@EDG: CAP_S7|next|CAP_S8
@EDG: CAP_S8|next|CAP_S9
@EDG: CAP_S9|next|CAP_S10
@EDG: CAP_S10|next|CAP_S11
@EDG: CAP_S11|next|CAP_S12
@EDG: CAP_S12|next|CAP_S13

# ---------- DATA:HEADer? fields ----------

@CLM: HDR_F1|pos=1|x_start seconds; time of first sample|persistent
@CLM: HDR_F2|pos=2|x_stop seconds; time of last sample|persistent
@CLM: HDR_F3|pos=3|record_length; sample count|persistent
@CLM: HDR_F4|pos=4|vals_per_sample; 1 normal, 2 peak/envelope pairs|persistent

# ---------- Common pitfalls (trap -> fix -> rule) ----------

@CLM: PIT_01|trap|TRIG:MODE SING|persistent
@CLM: FIX_01|fix|TRIGger:MODE NORMal + RUNsingle|persistent
@EDG: PIT_01|correctedBy|FIX_01
@EDG: PIT_01|violates|R04

@CLM: PIT_02|trap|TRIG:EVEN1:SOUR C1|persistent
@CLM: FIX_02|fix|TRIGger:EVENt1:SOURce CHANnel1|persistent
@EDG: PIT_02|correctedBy|FIX_02
@EDG: PIT_02|violates|R01

@CLM: PIT_03|trap|TRIG:EVEN1:LEV1 regardless of source|persistent
@CLM: FIX_03|fix|TRIGger:EVENt1:LEVel<n> where n = source channel|persistent
@EDG: PIT_03|correctedBy|FIX_03

@CLM: PIT_04|trap|CHAN1:DATA?|persistent
@CLM: FIX_04|fix|CHANnel1:WAVeform1:DATA:VALues?|persistent
@EDG: PIT_04|correctedBy|FIX_04
@EDG: PIT_04|violates|R02

@CLM: PIT_05|trap|binary read without FORMat:DATA set|persistent
@CLM: FIX_05|fix|send REAL,32 + LSBFirst before every read|persistent
@EDG: PIT_05|correctedBy|FIX_05
@EDG: PIT_05|violates|R07

@CLM: PIT_06|trap|hard-coded ACQ:POIN minimum|persistent
@CLM: FIX_06|fix|query ACQuire:POINts? MIN and MAX|persistent
@EDG: PIT_06|correctedBy|FIX_06

@CLM: PIT_07|trap|TIMebase:REFerence 0.5 as fraction|persistent
@CLM: FIX_07|fix|TIMebase:REFerence 50 (percent)|persistent
@EDG: PIT_07|correctedBy|FIX_07

@CLM: PIT_08|trap|AUToscale in scripts|persistent
@CLM: FIX_08|fix|explicit scales; TRIGger:FINDlevel for level only|persistent
@EDG: PIT_08|correctedBy|FIX_08
@EDG: PIT_08|violates|R03

@CLM: PIT_09|trap|ACQ:SRAT silently follows ACQ:POIN|persistent
@CLM: FIX_09|fix|set both ACQuire:POINts:MODE and ACQuire:SRATe:MODE to MANual|persistent
@EDG: PIT_09|correctedBy|FIX_09

@CLM: PIT_10|trap|ignoring SYST:ERR?|persistent
@CLM: FIX_10|fix|drain after connect, apply, *OPC?, each binary read|persistent
@EDG: PIT_10|correctedBy|FIX_10
@EDG: PIT_10|violates|R05

@CLM: PIT_11|trap|hard-coded time axis|persistent
@CLM: FIX_11|fix|parse DATA:HEADer?|persistent
@EDG: PIT_11|correctedBy|FIX_11
@EDG: PIT_11|violates|R08

@CLM: PIT_12|trap|ignoring vals_per_sample=2|persistent
@CLM: FIX_12|fix|split into min/max traces|persistent
@EDG: PIT_12|correctedBy|FIX_12
@EDG: PIT_12|violates|R09

@CLM: PIT_13|trap|*RST at connect|persistent
@CLM: FIX_13|fix|only on explicit user reset action|persistent
@EDG: PIT_13|correctedBy|FIX_13
@EDG: PIT_13|violates|R10

# ---------- Families ----------

@SET: family_modern|MXO4|MXO5|RTO|RTO6|RTP|persistent
@SET: family_legacy|RTM|RTA|persistent

@CLM: TRG_MODEL_MOD|model=modern|TRIGger:EVENt<n>:{SOURce|TYPE|LEVel<n>|EDGE:SLOPe}|persistent
@CLM: TRG_MODEL_LEG|model=legacy|TRIGger:A:{MODE|SOURce|TYPE|LEVel<n>:VALue|EDGE:SLOPe}|persistent

@EDG: family_modern|usesTriggerModel|TRG_MODEL_MOD
@EDG: family_legacy|usesTriggerModel|TRG_MODEL_LEG

@RUL: R11|MUSTNOT|mix EVENt<n> and A: trigger models in one driver; detect from *IDN?|high|persistent

# ---------- Family-specific enums ----------

@CLM: ACQ_TYPE|enum|SAMPle|PDETect|HRESolution|AVERage|ENVelope|persistent
@CLM: ACQ_INT|enum|SINX|LINear|SMHD|persistent
@CLM: TRG_MODE|enum|AUTO|NORMal|FREerun|persistent
@CLM: FMT_DATA|enum|REAL,32|ASCii|INT,16|persistent
@CLM: FMT_BORD|enum|LSBFirst|MSBFirst|persistent
@CLM: COUP_MOD|enum|DC|AC|GND (MXO firmware may accept DCLimit|ACLimit|GND)|persistent
@CLM: COUP_LEG|enum|DCLimit|ACLimit|GND (RTM/RTA)|persistent

@EDG: family_modern|couplingEnum|COUP_MOD
@EDG: family_legacy|couplingEnum|COUP_LEG

# ---------- Waveform data commands ----------

@CLM: WAV_HDR|cmd|CHANnel<n>:WAVeform<w>:DATA:HEADer?|persistent
@CLM: WAV_VAL|cmd|CHANnel<n>:WAVeform<w>:DATA:VALues?|persistent
@CLM: WAV_CHK|cmd|CHANnel<n>:WAVeform<w>:DATA:VALues? <offset>,<length>|persistent

# ---------- Transport matrix ----------

@ROU: RS_VISA|bench default; HiSLIP; robust binary; SelectVisa='rs'
@ROU: NI_VISA|windows without R&S VISA; slower on long records
@ROU: pyvisa_py|CI / minimal env; manual #N header decode; small records
@ROU: RsInstrument|prefer for binary; wraps chunking, timeouts, byte order

@RUL: R12|MUST|visa_timeout >= 60000 ms for large DATA:VALues?|high|persistent
@RUL: R13|MUST|opc_timeout >= 10000 ms if AUToset/AUToscale ever used|med|persistent

# ---------- Debugging playbook ----------

@PRC: DBG_1|log every SCPI line and every response|persistent
@PRC: DBG_2|drain SYSTem:ERRor:NEXT? until +0,"No error"; record all|persistent
@PRC: DBG_3|query FORMat:DATA? and FORMat:BORDer? on instrument (not local memory)|persistent
@PRC: DBG_4|if *OPC? hangs: check TRIGger:MODE? and STATus:OPERation:CONDition?|persistent
@PRC: DBG_5|on enum surprise: round-trip echoed value; capture SYSTem:VERSion?|persistent

@EDG: DBG_1|next|DBG_2
@EDG: DBG_2|next|DBG_3
@EDG: DBG_3|next|DBG_4
@EDG: DBG_4|next|DBG_5

# ---------- Retrieval seeds ----------

@IDX: rs_scpi_seeds|count=30|R&S SCPI|Rohde & Schwarz|MXO4|MXO5|RTO|RTO6|RTP|RTM|RTA|oscilloscope SCPI|RsInstrument|HiSLIP|VISA|DATA:HEADer|WAVeform1|RUNsingle|TRIGger:EVENt|TRIGger:MODE|ACQuire:POINts|ACQuire:SRATe|ACQuire:TYPE|TIMebase:REFerence|FORMat:DATA|FORMat:BORDer|SYST:ERR|long-form SCPI|binary block|peak detect|vals_per_sample|persistent
```
