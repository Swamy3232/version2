"""
orosunit.ini file converted to string using https://www.pythonescaper.com/
"""

orosunit_str = r"""; ----------------------------------------------------------------------------
;	NVGate definition : Unit and magnitude
; 	Version 2.3
; 	Date : December 2nd 2005
;   The 0 dB Reference values are complying with ISO 1683.2
; ----------------------------------------------------------------------------

; ---------------------------------------------------
; WARNING - WARNING - WARNING - WARNING
;	Modifying this file will avoid NVGate warranty
;	and may cause troubles
;----------------------------------------------------

; Possible values for Notation parameter
;	0 = Fixed (Default)
;	1 = Prefixed
;	2 = Engineer
;	3 = Scientific
;	4 = Time
;
; Possible values of ScaleAuthorized parameter
;	1 = Lin Scale
;	2 = Log Scale
;	4 = dB Scale
;   7 = All scale authorized
;   5 = Lin and dB scales authorized
;
; Possible values for SettingUnit parameter. It enables the setting to be set in dB
;	0 = Only linear
;	1 = Linear or dB, Linear is prefered
;	2 = Linear or dB, dB is prefered

; ----------------------------------------------------------------------
;					List of available magnitudes
; ----------------------------------------------------------------------

[BASE QUANTITY]
Number = 60
Quantity1 = None
Quantity2 = Acceleration
Quantity3 = Velocity
Quantity4 = Percentage
Quantity5 = Frequency
Quantity6 = Potential_Difference
Quantity7 = Angular_Velocity
Quantity8 = Length
Quantity9 = Pressure
Quantity10 = Force
Quantity11 = Accoustic_Pressure
Quantity12 = Intensity
Quantity13 = Time
Quantity14 = Ratio
Quantity15 = Plane_Angle
Quantity16 = Phase
Quantity17 = Square_Root_Frequency
Quantity18 = Sampling_Frequency
Quantity19 = Coherence
Quantity20 = Temperature
Quantity21 = Couple
Quantity22 = Power
Quantity23 = Resistance
Quantity24 = Conductance
Quantity25 = Ordre
Quantity26 = Sampling_Angle
Quantity27 = Sweep_Speed_Linear
Quantity28 = Sweep_Speed_Log
Quantity29 = Phase_Variation_Rate
Quantity30 = Log_Step
Quantity31 = Debit
Quantity32 = Strain
Quantity33 = Undefined_Magnitude
Quantity34 = Slice_Number
Quantity35 = Magnetic_Flux
Quantity36 = Temperature_Kelvin
Quantity37 = Temperature_Fahrenheit
Quantity38 = Spare1
Quantity39 = Spare2
Quantity40 = Spare3
Quantity41 = Spare4
Quantity42 = Quefrency
Quantity43 = YCepstrum
Quantity44 = Mass
Quantity45 = Surface
Quantity46 = Volume
Quantity47 = Delay
Quantity48 = Angular_Acceleration
Quantity49 = Torsional_Angle
Quantity50 = Torsional_Velocity
Quantity51 = Torsional_Acceleration
Quantity52 = Delay_Angle
Quantity53 = RoDer
Quantity54 = Loudness
Quantity55 = Sharpness
Quantity56 = Roughness
Quantity57 = Fluctuation_Strength
Quantity58 = Frequency_Group
Quantity59 = Loudness_Level
Quantity60 = Specific_Loudness

; ----------------------------------------------------------------------
;					MAGNITUDE DEFINITION
; ----------------------------------------------------------------------

;	--- Grandeur sans unité ---
;-------------------------------
[None]
Id = 1
Ids = 10001
EqDim = m:0
Number = 1
Unit1 = NoUnits
TypeUFF = 0
SettingUnit = 1

;	--- Accelération  ---
;--------------------------
[Acceleration]
Id = 2
Ids = 10002
EqDim = m:1|s:-2
Number = 4
Unit1 = M/s2
Unit2 = G
Unit3 = In/s2
Unit4 = Ft/s2
TypeUFF = 12
SettingUnit = 0

;	--- Vitesse  ---
;--------------------------
[Velocity]
Id = 3
Ids = 10003
EqDim = m:1|s:-1
Number = 6
Unit1 = M/s
Unit2 = Km/h
Unit3 = Mph
Unit4 = Ips
Unit5 = mm/s
Unit6 = µm/s
TypeUFF = 11
SettingUnit = 0

;	--- Pourcentage  ---
;--------------------------
[Percentage]
Id = 4
Ids = 10004
EqDim = m:0
Number = 1
Unit1 = Percent
TypeUFF = 0
SettingUnit = 0

;	--- Fréquence ---
;--------------------------
[Frequency]
Id = 5
Ids = 10005
EqDim = s:-1
Number = 2
Unit1 = Hertz
Unit2 = Cycle/min
TypeUFF = 18
SettingUnit = 0

;	--- Difference de potentiel ---
;-------------------------------------
[Potential_Difference]
Id = 6
Ids = 10006
EqDim = m:2|kg:1|s:-3|A:-1
Number = 1
Unit1 = Volt
TypeUFF = 1
SettingUnit = 1
IsReference = 1

;	--- Vitesse angulaire ---
;--------------------------------
[Angular_Velocity]
Id = 7
Ids = 10007
EqDim = rad:1|s:-1
Number = 3
Unit1 = Rad/sec
Unit2 = RPM
Unit3 = Deg/sec
TypeUFF = 19
SettingUnit = 0
CurrentUnit = 2
IsReference = 1

;	--- Longueur ---
;-----------------------
[Length]
Id = 8
Ids = 10008
EqDim = m:1
Number = 6
Unit1 = Meter
Unit2 =	Inch
Unit3 = Mils
Unit4 = Centimeter
Unit5 = Micron
Unit6 = Millimeter
TypeUFF = 8
SettingUnit = 0
IsReference = 1

;	--- Pression ---
;-----------------------
[Pressure]
Id = 9
Ids = 10009
EqDim = m:-1|kg:1|s:-2
Number = 3
Unit1 = N/m2
Unit2 = PSI
Unit3 = Atm
TypeUFF = 15
SettingUnit = 0
IsReference = 1

;	--- Force ---
;---------------------
[Force]
Id = 10
Ids = 10010
EqDim = m:1|kg:1|s:-2
Number = 3
Unit1 = Newton
Unit2 = Pounds_force
Unit3 = Dynes
TypeUFF = 13
SettingUnit = 0

;	--- Pression accoustique ---
;-----------------------------------
[Accoustic_Pressure]
Id = 11
Ids = 10011
EqDim = m:-1|kg:1|s:-2
Number = 2
Unit1 = Pascal
Unit2 = Bar
TypeUFF = 15
SettingUnit = 2

;	--- Intensité electrique ---
;-----------------------------------
[Intensity]
Id = 12
Ids = 10012
EqDim = A:1
Number = 1
Unit1 = Ampere
TypeUFF = 0
SettingUnit = 0
IsReference = 1

;	--- Temps---
;-------------------
[Time]
Id = 13
Ids = 10013
EqDim = s:1
Number = 3
Unit1 = Seconde
Unit2 = Minute
Unit3 = Hour
TypeUFF = 17
SettingUnit = 0
IsReference = 1

;	--- Delay---
;-------------------
[Delay]
Id = 47
Ids = 10047
EqDim = s:1
Number = 3
Unit1 = Seconde
Unit2 = Minute
Unit3 = Hour
TypeUFF = 17
SettingUnit = 0
IsReference = 1

;	--- Ratio de valeurs ---
;-------------------------------
[Ratio]
Id = 14
Ids = 10014
EqDim = m:0
Number = 2
Unit1 = Decibel
Unit2 = Percent
TypeUFF = 0
SettingUnit = 0

;	--- Angle ---
;-------------------------------
[Plane_Angle]
Id = 15
Ids = 10015
EqDim = rad:1
Number = 2
Unit1 = Radian
Unit2 = Degree
TypeUFF = 0
SettingUnit = 0
CurrentUnit = 2

;	--- Phase ---
;-------------------------------
[Phase]
Id = 16
Ids = 10016
EqDim = rad:1
Number = 2
Unit1 = Radian
Unit2 = Degree
TypeUFF = 0
SettingUnit = 0
CurrentUnit = 2

;	--- Racine carrée de Hertz ---
;-------------------------------
[Square_Root_Frequency]
Id = 17
Ids = 10017
EqDim = s:-0.5
Number = 2
Unit1 = Square_Root_Hertz
Unit2 = Square_Root_CPM
TypeUFF = 0
SettingUnit = 0

;	--- Fréquence d'échantillonnage ---
;--------------------------
[Sampling_Frequency]
Id = 18
Ids = 10018
EqDim = m:0
Number = 1
Unit1 = Sample/s
TypeUFF = 18
SettingUnit = 0

;	--- Representation de la coherence ---
;--------------------------
[Coherence]
Id = 19
Ids = 10019
EqDim = m:0
Number = 2
Unit1 = Coherence_01
Unit2 = Percent
TypeUFF = 0
SettingUnit = 0
CurrentUnit = 2

;	--- Temperature ---
;--------------------------
[Temperature]
Id = 20
Ids = 10020
EqDim = K:1
Number = 1
Unit1 = Celsius
TypeUFF = 5
SettingUnit = 0
IsReference = 1

;	--- Couple (Torque ou Moment) ---
;--------------------------
[Couple]
Id = 21
Ids = 10021
EqDim = m:2|kg:1|s:-2
Number = 1
Unit1 = NewtonMeter
TypeUFF = 0
SettingUnit = 0
IsReference = 1

;	--- Puissance Electrique ---
;--------------------------
[Power]
Id = 22
Ids = 10022
EqDim = m:2|kg:1|s:-3
Number = 1
Unit1 = Watt
TypeUFF = 0
SettingUnit = 0
IsReference = 1

;	--- Résistance Electrique ---
;--------------------------
[Resistance]
Id = 23
Ids = 10023
EqDim = m:2|kg:1|s:-3|A:-2
Number = 1
Unit1 = Ohm
TypeUFF = 0
SettingUnit = 0
IsReference = 1

;	--- Conductance Electrique ---
;--------------------------
[Conductance]
Id = 24
Ids = 10024
EqDim = m:-2|kg:-1|s:3|A:1
Number = 1
Unit1 = Siemens
TypeUFF = 0
SettingUnit = 0
IsReference = 1

;	--- Ordre ---
;--------------------------
[Ordre]
Id = 25
Ids = 10025
EqDim = m:0
Number = 1
Unit1 = UniteOrdre
TypeUFF = 0
SettingUnit = 0

;	--- Sampling_Angle ---
;-------------------------------
[Sampling_Angle]
Id = 26
Ids = 10026
EqDim = rad:1
Number = 4
Unit1 = SamplingRevolution
Unit2 = SamplingGrade
Unit3 = SamplingRadian
Unit4 = SamplingDegree
TypeUFF = 0
SettingUnit = 0

;	--- Delay_Angle ---
;-------------------------------
[Delay_Angle]
Id = 52
Ids = 10052
EqDim = rad:1
Number = 4
Unit1 = SamplingRevolution
Unit2 = SamplingGrade
Unit3 = SamplingRadian
Unit4 = SamplingDegree
TypeUFF = 0
SettingUnit = 0

;	--- RoDer ---
;-------------------------------
[RoDer]
Id = 53
Ids = 10053
EqDim = rad:1
Number = 4
Unit1 = SamplingRevolution
Unit2 = SamplingGrade
Unit3 = SamplingRadian
Unit4 = SamplingDegree
TypeUFF = 0
SettingUnit = 0

;	--- Loudness ---
;-------------------------------
[Loudness]
Id = 54
Ids = 10054
EqDim = m:0
Number = 1
Unit1 = Sone
TypeUFF = 0
SettingUnit = 0

;	--- Sharpness ---
;-------------------------------
[Sharpness]
Id = 55
Ids = 10055
EqDim = m:0
Number = 1
Unit1 = Acum
TypeUFF = 0
SettingUnit = 0

;	--- Roughness ---
;-------------------------------
[Roughness]
Id = 56
Ids = 10056
EqDim = m:0
Number = 1
Unit1 = Asper
TypeUFF = 0
SettingUnit = 0

;	--- Fluctuation_Strength ---
;-------------------------------
[Fluctuation_Strength]
Id = 57
Ids = 10057
EqDim = m:0
Number = 1
Unit1 = Vacil
TypeUFF = 0
SettingUnit = 0

;	--- Frequency_Group ---
;-------------------------------
[Frequency_Group]
Id = 58
Ids = 10058
EqDim = s:-1
Number = 1
Unit1 = Bark
TypeUFF = 0
SettingUnit = 0

;	--- Loudness_Level ---
;-------------------------------
[Loudness_Level]
Id = 59
Ids = 10059
EqDim = m:0
Number = 1
Unit1 = Phon
TypeUFF = 0
SettingUnit = 0

;	--- Specific_Loudness ---
;-------------------------------
[Specific_Loudness]
Id = 60
Ids = 10060
EqDim = s:1
Number = 1
Unit1 = SonePerBark
TypeUFF = 0
SettingUnit = 0

;	--- Vitesse de variation de frequence en lineaire ---
;-------------------------------
[Sweep_Speed_Linear]
Id = 27
Ids = 10027
EqDim =  s:-2
Number = 1
Unit1 = Hertz_Per_Second
TypeUFF = 0
SettingUnit = 0


;	--- Vitesse de variation de frequence en log ---
;-------------------------------
[Sweep_Speed_Log]
Id = 28
Ids = 10028
EqDim =  s:-2
Number = 2
Unit1 = Decade_Per_Second
Unit2 = Octave_Per_Minut
TypeUFF = 0
SettingUnit = 0

;	--- Vitesse de variation de phase en lin ---
;-------------------------------
[Phase_Variation_Rate]
Id = 29
Ids = 10029
EqDim =  s:-1
Number = 2
Unit1 = Rad/sec
Unit2 = Deg/sec
TypeUFF = 0
SettingUnit = 0
CurrentUnit = 2

;	--- Nombre de points sur une bande de frequence ---
;-------------------------------
[Log_Step]
Id = 30
Ids = 10030
EqDim =  mol:1|s:1
Number = 1
Unit1 = Point_Per_Decade
TypeUFF = 0
SettingUnit = 0

;	--- Debit  ---
;--------------------------
[Debit]
Id = 31
Ids = 10031
EqDim = m:3|s:-1
Number = 1
Unit1 = M3/s
TypeUFF = 0
SettingUnit = 0
IsReference = 1

;	--- Strain ---
;-------------------------------
[Strain]
Id = 32
Ids = 10032
EqDim = m:0
Number = 1
Unit1 = Deformation
TypeUFF = 3
SettingUnit = 0
IsReference = 1
CurrentUnit = 1

;	--- Undefined magnitude ---
;-------------------------------
[Undefined_Magnitude]
Id = 33
Ids = 10033
EqDim = m:0
Number = 1
Unit1 = EU
TypeUFF = 0
SettingUnit = 0
IsReference = 1

;	--- Slice Number ---
;-------------------------------
[Slice_Number]
Id = 34
Ids = 10034
EqDim = m:0
Number = 1
Unit1 = SHARP
TypeUFF = 0
SettingUnit = 0
IsReference = 1

;     --- Magnetic_Flux ---
;-------------------------------
[Magnetic_Flux]
Id = 35
Ids = 10035
EqDim = kg:1|s:-2|A:-1
Number = 1
Unit1 = Tesla
TypeUFF = 0
SettingUnit = 0
IsReference = 1

;	--- Temperature in Kelvin---
;--------------------------
[Temperature_Kelvin]
Id = 36
Ids = 10036
EqDim = K:1
Number = 1
Unit1 = Kelvin
TypeUFF = 5
SettingUnit = 0
IsReference = 1

;	--- Temperature in Fahrenheit---
;--------------------------
[Temperature_Fahrenheit]
Id = 37
Ids = 10037
EqDim = K:1
Number = 1
Unit1 = Fahrenheit
TypeUFF = 5
SettingUnit = 0
IsReference = 1

;	--- User free---
;--------------------------
[Spare1]
Id = 38
Ids = 10038
EqDim = m:0
Number = 1
Unit1 = NoUnits
TypeUFF = 0
SettingUnit = 1

;	--- User free---
;--------------------------
[Spare2]
Id = 39
Ids = 10039
EqDim = m:0
Number = 1
Unit1 = NoUnits
TypeUFF = 0
SettingUnit = 1

;	--- User free---
;--------------------------
[Spare3]
Id = 40
Ids = 10040
EqDim = m:0
Number = 1
Unit1 = NoUnits
TypeUFF = 0
SettingUnit = 1

;	--- User free---
;--------------------------
[Spare4]
Id = 41
Ids = 10041
EqDim = m:0
Number = 1
Unit1 = NoUnits
TypeUFF = 0
SettingUnit = 1


;	--- Quefrency ---
;--------------------------
[Quefrency]
Id = 42
Ids = 10042
EqDim = s:1
Number = 2
Unit1 = Seconde
Unit2 = InvHertz
TypeUFF = 0
SettingUnit = 0

;	--- YCepstrum ---
;--------------------------
[YCepstrum]
Id = 43
Ids = 10043
EqDim = m:0
Number = 1
Unit1 = DecibelCepstrum
TypeUFF = 0
SettingUnit = 0

;	--- Mass ---
;--------------------------
[Mass]
Id = 44
Ids = 10044
EqDim = kg:1
Number = 2
Unit1  = KiloGram
Unit2  = Gram
TypeUFF = 16
SettingUnit = 0

;	--- Surface ---
;--------------------------
[Surface]
Id = 45
Ids = 10045
EqDim = m:2
Number = 2
Unit1  = SquareMeters
Unit2  = SquareMilliMeters
TypeUFF = 0
SettingUnit = 0

;	--- Volume ---
;--------------------------
[Volume]
Id = 46
Ids = 10046
EqDim = m:3
Number = 2
Unit1  = CubicMeters
Unit2  = Liter
TypeUFF = 0
SettingUnit = 0

;	--- Acceleration angulaire ---
;--------------------------------
[Angular_Acceleration]
Id = 48
Ids = 10048
EqDim = rad:1|s:-2
Number = 3
Unit1 = Rad/s2
Unit2 = RPM/s
Unit3 = Deg/s2
TypeUFF = 0
SettingUnit = 0
CurrentUnit = 2
IsReference = 1

;	--- Torsional Angle ---
;-------------------------------
[Torsional_Angle]
Id = 49
Ids = 10049
EqDim = rad:1
Number = 2
Unit1 = Radian
Unit2 = Degree
TypeUFF = 0
SettingUnit = 0
CurrentUnit = 2

;	--- Torsional Vitesse ---
;--------------------------------
[Torsional_Velocity]
Id = 50
Ids = 10050
EqDim = rad:1|s:-1
Number = 2
Unit1 = Rad/sec
Unit2 = Deg/sec
TypeUFF = 19
SettingUnit = 0
CurrentUnit = 2
IsReference = 1

;	--- Torsional Acceleration ---
;--------------------------------
[Torsional_Acceleration]
Id = 51
Ids = 10051
EqDim = rad:1|s:-2
Number = 2
Unit1 = Rad/s2
Unit2 = Deg/s2
TypeUFF = 0
SettingUnit = 0
CurrentUnit = 2
IsReference = 1

; ----------------------------------------------------------------------
;					END OF MAGNITUDE DEFINITION
; ----------------------------------------------------------------------

; ----------------------------------------------------------------------
;						UNIT DEFINITION
; ----------------------------------------------------------------------

;	--- Sans Unité ---
[NoUnits]
Id = 1
Ids = 11001
LabelLin =
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = -12
HigherPrefix = 9
ScaleAuthorized = 7

;	--- metre / seconde au carré ---
[M/s2]
Id = 2
Ids = 11002
LabelLin = m/s²
CoeffA = 1
CoeffB = 0
Ref0dB = 1e-6
CoeffdB = 20
NoZeroRight = 1
Notation = 1
LowerPrefix = -12
HigherPrefix = 3
ScaleAuthorized = 7

;	--- gé ---
[G]
Id = 3
Ids = 11003
LabelLin = g
CoeffA = 0.1019368
CoeffB = 0
Ref0dB = 101.9368e-9
CoeffdB = 20
NoZeroRight = 1
Notation = 1
LowerPrefix = -12
HigherPrefix = 6
ScaleAuthorized = 7


;	--- inch / seconde au carré ---
[In/s2]
Id = 4
Ids = 11004
LabelLin = inch/s²
CoeffA = 39.37008
CoeffB = 0
Ref0dB = 39.37008e-6
CoeffdB = 20
NoZeroRight = 1
Notation = 2
LowerPrefix = 0
HigherPrefix = 0
ScaleAuthorized = 7

;	--- metre par seconde ---
[M/s]
Id = 5
Ids = 11005
LabelLin = m/s
CoeffA = 1
CoeffB = 0
Ref0dB = 1e-9
CoeffdB = 20
NoZeroRight = 0
Notation = 1
LowerPrefix = -12
HigherPrefix = 3
ScaleAuthorized = 7

;	--- kilometre par heure ---
[Km/h]
Id = 6
Ids = 11006
LabelLin = km/h
CoeffA = 3.6
CoeffB = 0
Ref0dB = 3.6e-9
CoeffdB = 20
NoZeroRight = 0
Notation = 0
LowerPrefix = 0
HigherPrefix = 0
ScaleAuthorized = 7

;	--- miles par heure ---
[Mph]
Id = 7
Ids = 11007
LabelLin = mph
CoeffA = 2.2369362920544
CoeffB = 0
Ref0dB = 2.2369362920544e-9
CoeffdB = 20
NoZeroRight = 0
Notation = 0
LowerPrefix = 0
HigherPrefix = 0
ScaleAuthorized = 7

;	--- pourcentage ---
[Percent]
Id = 8
Ids = 11008
LabelLin = %
CoeffA = 100
CoeffB = 0
Ref0dB = 100
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = 0
HigherPrefix = 0
ScaleAuthorized = 3

;	--- Hertz ---
[Hertz]
Id = 9
Ids = 11009
LabelLin = Hz
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 1
LowerPrefix = -9
HigherPrefix = 6
ScaleAuthorized = 3

;	--- Volt ---
[Volt]
Id = 10
Ids = 11010
LabelLin = V
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 1
LowerPrefix = -12
HigherPrefix = 9
ScaleAuthorized = 7

;	--- cycle par minute ---
[Cycle/min]
Id = 11
Ids = 11011
LabelLin = Cyc/min
CoeffA = 60
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 1
LowerPrefix = 0
HigherPrefix = 3
ScaleAuthorized = 3

;	--- radian par seconde ---
[Rad/sec]
Id = 12
Ids = 11012
LabelLin = rad/s
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 1
LowerPrefix = -9
HigherPrefix = 0
ScaleAuthorized = 3

;	--- metre ---
[Meter]
Id = 13
Ids = 11013
LabelLin = m
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 0
Notation = 1
LowerPrefix = -12
HigherPrefix = 3
ScaleAuthorized = 7

;	--- inche ---
[Inch]
Id = 14
Ids = 11014
LabelLin = in
CoeffA = 39.37007874
CoeffB = 0
Ref0dB = 39.37007874
CoeffdB = 20
NoZeroRight = 0
Notation = 0
LowerPrefix = 0
HigherPrefix = 0
ScaleAuthorized = 7

;	--- millieme d'inche ---
[Mils]
Id = 15
Ids = 11015
LabelLin = mils
CoeffA = 39370.07874
CoeffB = 0
Ref0dB = 39370.07874
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = 0
HigherPrefix = 0
ScaleAuthorized = 7

;	--- Pascal ---
[Pascal]
Id = 16
Ids = 11016
LabelLin = Pa
CoeffA = 1
CoeffB = 0
Ref0dB = 2e-5
CoeffdB = 20
NoZeroRight = 1
Notation = 2
LowerPrefix = -12
HigherPrefix = 9
ScaleAuthorized = 7

;	--- bar ---
[Bar]
Id = 17
Ids = 11017
LabelLin = bar
CoeffA = 1e-5
CoeffB = 0
Ref0dB = 2e-10
CoeffdB = 20
NoZeroRight = 0
Notation = 1
LowerPrefix = -6
HigherPrefix = 0
ScaleAuthorized = 7

;	--- Newton ---
[Newton]
Id = 18
Ids = 11018
LabelLin = N
CoeffA = 1
CoeffB = 0
Ref0dB = 1e-6
CoeffdB = 20
NoZeroRight = 1
Notation = 1
LowerPrefix = -12
HigherPrefix = 9
ScaleAuthorized = 5

;	--- Ampere ---
[Ampere]
Id = 19
Ids = 11019
LabelLin = A
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 1
LowerPrefix = -12
HigherPrefix = 9
ScaleAuthorized = 7

;	--- Seconde ---
[Seconde]
Id = 20
Ids = 11020
LabelLin = s
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 1
LowerPrefix = -12
HigherPrefix = 0
ScaleAuthorized = 1

;	--- Minute ---
[Minute]
Id = 21
Ids = 11021
LabelLin = min
CoeffA = 0.016666666
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = 0
HigherPrefix = 0
ScaleAuthorized = 1

;	--- Heure ---
[Hour]
Id = 22
Ids = 11022
LabelLin = hour
CoeffA = 0.0002777777
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = 0
HigherPrefix = 0
ScaleAuthorized = 1

;	--- Decibel ---
[Decibel]
Id = 23
Ids = 11023
LabelLin = dB
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 0
Notation = 0
LowerPrefix = 0
HigherPrefix = 0
ScaleAuthorized = 4

;	--- centimetre ---
[Centimeter]
Id = 24
Ids = 11024
LabelLin = cm
CoeffA = 100
CoeffB = 0
Ref0dB = 100
CoeffdB = 20
NoZeroRight = 0
Notation = 0
LowerPrefix = 0
HigherPrefix = 0
ScaleAuthorized = 7

;	--- radian ---
[Radian]
Id = 25
Ids = 11025
LabelLin = rad
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 1
LowerPrefix = -12
HigherPrefix = 0
ScaleAuthorized = 3

;	--- degré d'angle ---
[Degree]
Id = 26
Ids = 11026
LabelLin = °
CoeffA = 57.29577951
CoeffB = 0
Ref0dB = 57.29577951
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = 0
HigherPrefix = 0
ScaleAuthorized = 3

;	--- Racine de Hertz ---
[Square_Root_Hertz]
Id = 27
Ids = 11027
LabelLin = Hz½
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = -9
HigherPrefix = 6
ScaleAuthorized = 1

;	--- Racine de cycle par minutes ---
[Square_Root_CPM]
Id = 28
Ids = 11028
LabelLin = (Cyc/min)½
CoeffA = 7.74596669
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = -3
HigherPrefix = 6
ScaleAuthorized = 1

;	--- RPM ---
[RPM]
Id = 29
Ids = 11029
LabelLin = RPM
CoeffA = 9.5492965
CoeffB = 0
Ref0dB = 9.5492965
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = -9
HigherPrefix = 6
ScaleAuthorized = 3

;	--- N/m2 ---
[N/m2]
Id = 30
Ids = 11030
LabelLin = N/m²
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = -9
HigherPrefix = 6
ScaleAuthorized = 3

;	--- Inch / s ---
[Ips]
Id = 31
Ids = 11031
LabelLin = Ips
CoeffA = 39.37007874
CoeffB = 0
Ref0dB = 39.37007874e-9
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = -9
HigherPrefix = 6
ScaleAuthorized = 7

;	--- Sample / s ---
[Sample/s]
Id = 32
Ids = 11032
LabelLin = S/s
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 1
LowerPrefix = 0
HigherPrefix = 3
ScaleAuthorized = 1

;	--- Sans dimension, pour la coherence ---
[Coherence_01]
Id = 33
Ids = 11033
LabelLin =
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = 0
HigherPrefix = 0
ScaleAuthorized = 3

;	--- Kelvin ---
[Kelvin]
Id = 34
Ids = 11034
LabelLin = K
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = 0
HigherPrefix = 0
ScaleAuthorized = 1

;	--- °C ---
[Celsius]
Id = 35
Ids = 11035
LabelLin = °C
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = 0
HigherPrefix = 0
ScaleAuthorized = 1

;	--- Fahrenheit ---
[Fahrenheit]
Id = 36
Ids = 11036
LabelLin = F
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = 0
HigherPrefix = 0
ScaleAuthorized = 1

;	--- Newton mètre ---
[NewtonMeter]
Id = 37
Ids = 11037
LabelLin = Nm
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = 0
HigherPrefix = 0
ScaleAuthorized = 3
SettingUnit = 0

;	--- mm / s ---
[mm/s]
Id = 38
Ids = 11038
LabelLin = mm/s
CoeffA = 1000
CoeffB = 0
Ref0dB = 1e-6
CoeffdB = 20
NoZeroRight = 0
Notation = 2
LowerPrefix = -12
HigherPrefix = 3
ScaleAuthorized = 7

;	--- Watt ---
[Watt]
Id = 39
Ids = 11039
LabelLin = W
CoeffA = 1
CoeffB = 0
Ref0dB = 1e-3
CoeffdB = 10
NoZeroRight = 1
Notation = 1
LowerPrefix = -6
HigherPrefix = 12
ScaleAuthorized = 7

;	--- Ohm ---
[Ohm]
Id = 40
Ids = 11040
LabelLin = Ohm
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 1
LowerPrefix = -9
HigherPrefix = 6
ScaleAuthorized = 3

;	--- Siemens ---
[Siemens]
Id = 41
Ids = 11041
LabelLin = S
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 1
LowerPrefix = -9
HigherPrefix = 0
ScaleAuthorized = 3

;	--- UniteOrdre ---
[UniteOrdre]
Id = 42
Ids = 11042
LabelLin =
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = -12
HigherPrefix = 9
ScaleAuthorized = 1

;	--- tour pour reechantillonnage---
[SamplingRevolution]
Id = 43
Ids = 11043
LabelLin = rev
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 1
LowerPrefix = -12
HigherPrefix = 0
ScaleAuthorized = 1

;	--- Grade pour reechantillonnage ---
[SamplingGrade]
Id = 44
Ids = 11044
LabelLin = gr
CoeffA = 400
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 1
LowerPrefix = -12
HigherPrefix = 0
ScaleAuthorized = 1

;	--- degre pour reechantillonnage ---
[SamplingRadian]
Id = 45
Ids = 11045
LabelLin = rad
CoeffA = 6.2831853071795864
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 1
LowerPrefix = -12
HigherPrefix = 0
ScaleAuthorized = 1

;	--- degre pour reechantillonnage ---
[SamplingDegree]
Id = 46
Ids = 11046
LabelLin = °
CoeffA = 360
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = -12
HigherPrefix = 0
ScaleAuthorized = 1

;	--- Vitesse de variation de frequence en lineaire ---
[Hertz_Per_Second]
Id = 47
Ids = 11047
LabelLin = Hz/s
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 1
LowerPrefix = 0
HigherPrefix = 3
ScaleAuthorized = 1

;	--- Vitesse de variation de frequence en log ---
[Decade_Per_Second]
Id = 48
Ids = 11048
LabelLin = dec/s
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = 0
HigherPrefix = 0
ScaleAuthorized = 1

;	--- Vitesse de variation de frequence en log ---
[Octave_Per_Minut]
Id = 49
Ids = 11049
LabelLin = oct/min
CoeffA = 199.315685693241741		; 60*ln(10)/ln(2)
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = 0
HigherPrefix = 0
ScaleAuthorized = 1

;	--- Vitesse de variation de frequence en log ---
[Point_Per_Decade]
Id = 50
Ids = 11050
LabelLin = pt/dec
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = 0
HigherPrefix = 0
ScaleAuthorized = 1

;	--- radian par seconde ---
[Deg/sec]
Id = 51
Ids = 11051
LabelLin = deg/s
CoeffA = 57.29577951
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 1
LowerPrefix = -9
HigherPrefix = 0
ScaleAuthorized = 1

;	--- pound force ---
[Pounds_force]
Id = 52
Ids = 11052
LabelLin = lbF
CoeffA = 0.224808943
CoeffB = 0
Ref0dB = 224.808943e-9
CoeffdB = 20
NoZeroRight = 1
Notation = 2
LowerPrefix = -12
HigherPrefix = 9
ScaleAuthorized = 5

;	--- metre cube / seconde  ---
[M3/s]
Id = 53
Ids = 11053
LabelLin = m³/s
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 1
LowerPrefix = -12
HigherPrefix = 3
ScaleAuthorized = 7

;	--- Foot / seconde au carré ---
[Ft/s2]
Id = 54
Ids = 11054
LabelLin = ft/s²
CoeffA = 3.280840
CoeffB = 0
Ref0dB = 3.280840e-6
CoeffdB = 20
NoZeroRight = 1
Notation = 2
LowerPrefix = 0
HigherPrefix = 0
ScaleAuthorized = 7

;	--- pound force ---
[Dynes]
Id = 55
Ids = 11055
LabelLin = dynes
CoeffA = 100000
CoeffB = 0
Ref0dB = 0.1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = -12
HigherPrefix = 9
ScaleAuthorized = 5

;	--- Pound / inch² ---
[PSI]
Id = 56
Ids = 11056
LabelLin = psi
CoeffA = 0.000145
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = -9
HigherPrefix = 6
ScaleAuthorized = 3

;	--- Atmosphere ---
[Atm]
Id = 57
Ids = 11057
LabelLin = atm
CoeffA = 0.00001
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = -9
HigherPrefix = 6
ScaleAuthorized = 3

;	--- MicroDef ---
;[MicroDef]
;Id = 58
;Ids = 11058
;LabelLin = µdef
;CoeffA = 1e6
;CoeffB = 0
;Ref0dB = 1e6
;CoeffdB = 20
;NoZeroRight = 0
;Notation = 2
;LowerPrefix = 0
;HigherPrefix = 0
;ScaleAuthorized = 3

;	--- Engineering Unit ---
[EU]
Id = 59
Ids = 11059
LabelLin = EU
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = -12
HigherPrefix = 9
ScaleAuthorized = 7

;	--- Slice Number Unit ---
[SHARP]
Id = 60
Ids = 11060
LabelLin = #
CoeffA = 1
CoeffB = 1
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = -12
HigherPrefix = 9
ScaleAuthorized = 1

;      ----- Tesla ----
[Tesla]
Id = 61
Ids = 11061
LabelLin = T
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = -12
HigherPrefix = 9
ScaleAuthorized = 7

;	--- Hertz-1 ---
[InvHertz]
Id = 62
Ids = 11062
LabelLin = 1/Hz
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 1
LowerPrefix = -6
HigherPrefix = 9
ScaleAuthorized = 1

;	--- Decibel for cepstrum ---
[DecibelCepstrum]
Id = 63
Ids = 11063
LabelLin = dB
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 1
NoZeroRight = 0
Notation = 0
LowerPrefix = 0
HigherPrefix = 0
ScaleAuthorized = 3

;	--- Gram ---
[Gram]
Id = 64
Ids = 11064
LabelLin = g
CoeffA = 1000
CoeffB = 0
Ref0dB = 1
CoeffdB = 1
NoZeroRight = 0
Notation = 0
LowerPrefix = 0
HigherPrefix = 0

;	--- KiloGram ---
[KiloGram]
Id = 65
Ids = 11065
LabelLin = kg
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 1
NoZeroRight = 0
Notation = 0
LowerPrefix = 0
HigherPrefix = 0

;	--- SquareMeters ---
[SquareMeters]
Id = 66
Ids = 11066
LabelLin = m²
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 1
NoZeroRight = 0
Notation = 0
LowerPrefix = 0
HigherPrefix = 0

;	--- SquareMilliMeters ---
[SquareMilliMeters]
Id = 67
Ids = 11067
LabelLin = mm²
CoeffA = 1000000
CoeffB = 0
Ref0dB = 1
CoeffdB = 1
NoZeroRight = 0
Notation = 0
LowerPrefix = 0
HigherPrefix = 0

;	--- CubicMeters ---
[CubicMeters]
Id = 68
Ids = 11068
LabelLin = m³
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 1
NoZeroRight = 0
Notation = 0
LowerPrefix = 0
HigherPrefix = 0

;	--- Liter ---
[Liter]
Id = 69
Ids = 11069
LabelLin = l
CoeffA = 1000
CoeffB = 0
Ref0dB = 1
CoeffdB = 1
NoZeroRight = 0
Notation = 0
LowerPrefix = 0
HigherPrefix = 0

;	--- Micron ---
[Micron]
Id = 70
Ids = 11070
LabelLin = µm
CoeffA = 1e6
CoeffB = 0
Ref0dB = 1e6
CoeffdB = 20
NoZeroRight = 0
Notation = 0
LowerPrefix = 0
HigherPrefix = 0
ScaleAuthorized = 7

;	--- µm / s ---
[µm/s]
Id = 71
Ids = 11071
LabelLin = µm/s
CoeffA = 1e6
CoeffB = 0
Ref0dB = 1e-3
CoeffdB = 20
NoZeroRight = 0
Notation = 0
LowerPrefix = -12
HigherPrefix = 3
ScaleAuthorized = 7

;	--- radian par s² ---
[Rad/s2]
Id = 72
Ids = 11072
LabelLin = rad/s²
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 1
LowerPrefix = -9
HigherPrefix = 0
ScaleAuthorized = 3

;	--- degree par s² ---
[Deg/s2]
Id = 73
Ids = 11073
LabelLin = °/s²
CoeffA = 57.295780
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 1
LowerPrefix = -9
HigherPrefix = 0
ScaleAuthorized = 3

;	--- RPM par s ---
[RPM/s]
Id = 74
Ids = 11074
LabelLin = RPM/s
CoeffA = 9.549296
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 1
LowerPrefix = -9
HigherPrefix = 0
ScaleAuthorized = 3

;	--- Deformation ---
[Deformation]
Id = 75
Ids = 11075
LabelLin = def
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 0
Notation = 1
LowerPrefix = -6
HigherPrefix = -6
ScaleAuthorized = 3

;	--- millimeter ---
[Millimeter]
Id = 76
Ids = 11076
LabelLin = mm
CoeffA = 1000
CoeffB = 0
Ref0dB = 100
CoeffdB = 20
NoZeroRight = 0
Notation = 0
LowerPrefix = 0
HigherPrefix = 0
ScaleAuthorized = 7

;	--- sone for loudness ---
[Sone]
Id = 77
Ids = 11077
LabelLin = sone
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = -12
HigherPrefix = 9
ScaleAuthorized = 7

;	--- acum for sharpness ---
[Acum]
Id = 78
Ids = 11078
LabelLin = acum
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = -12
HigherPrefix = 9
ScaleAuthorized = 7

;	--- asper for roughness ---
[Asper]
Id = 79
Ids = 11079
LabelLin = asper
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = -12
HigherPrefix = 9
ScaleAuthorized = 7

;	--- vacil for fluctuationstrength ---
[Vacil]
Id = 80
Ids = 11080
LabelLin = vacil
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = -12
HigherPrefix = 9
ScaleAuthorized = 7

;	--- bark for frequencygroup ---
[Bark]
Id = 81
Ids = 11081
LabelLin = bark
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = -12
HigherPrefix = 9
ScaleAuthorized = 7

;	--- phon for loudness level ---
[Phon]
Id = 82
Ids = 11082
LabelLin = phon
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = -12
HigherPrefix = 9
ScaleAuthorized = 7

;	--- sone per bark for specific loudness ---
[SonePerBark]
Id = 83
Ids = 11083
LabelLin = sone/bark
CoeffA = 1
CoeffB = 0
Ref0dB = 1
CoeffdB = 20
NoZeroRight = 1
Notation = 0
LowerPrefix = -12
HigherPrefix = 9
ScaleAuthorized = 7

; ----------------------------------------------------------------------
;						END OF UNIT DEFINITION
; ----------------------------------------------------------------------

; ----------------------------------------------------------------------
;						Opérations sur les grandeurs
; ----------------------------------------------------------------------
[SIMPLIFICATION]
Number = 46
Simplification1 = Velocity              # Acceleration:1|Time:1
Simplification2 = Length                # Velocity:1|Time:1
Simplification3 = Length                # Acceleration:1|Time:2
Simplification4 = Potential_Difference  # Resistance:1|Intensity:1
Simplification5 = Power                 # Potential_Difference:1|Intensity:1
Simplification6 = Velocity              # Length:1|Time:-1
Simplification7 = Acceleration          # Velocity:1|Time:-1
Simplification8 = Acceleration          # Length:1|Time:-2
Simplification9 = Frequency             # Time:-1
Simplification10 = Time                 # Frequency:-1
Simplification11 = Potential_Difference # Resistance:1|Intensity:1
Simplification12 = Resistance           # Potential_Difference:1|Intensity:-1
Simplification13 = Intensity            # Potential_Difference:1|Resistance:-1
Simplification14 = Power		        # Potential_Difference:1|Intensity:1
Simplification15 = Potential_Difference # Power:1|Intensity:-1
Simplification16 = Intensity		    # Potential_Difference:-1|Power:1
Simplification17 = Power		        # Resistance:1|Intensity:2
Simplification18 = Power		        # Resistance:-1|Potential_Difference:2
Simplification19 = Resistance           # Power:1|Intensity:-2
Simplification20 = Resistance           # Power:-1|Potential_Difference:2
Simplification21 = Conductance          # Resistance:-1
Simplification22 = Resistance           # Conductance:-1
Simplification23 = Potential_Difference # Conductance:-1|Intensity:1
Simplification24 = Conductance          # Potential_Difference:-1|Intensity:1
Simplification25 = Intensity            # Potential_Difference:1|Conductance:1
Simplification26 = Power		        # Conductance:-1|Intensity:2
Simplification27 = Power		        # Conductance:1|Potential_Difference:2
Simplification28 = Conductance          # Power:-1|Intensity:2
Simplification29 = Conductance          # Power:1|Potential_Difference:-2
Simplification30 = Velocity             # Length:1|Frequency:1
Simplification31 = Force                # Pressure:1|Length:2
Simplification32 = Pressure             # Force:1|Length:-2
Simplification33 = Couple               # Force:1|Length:1
Simplification34 = Force                # Couple:1|Length:-1
Simplification35 = Length               # Couple:1|Force:-1
Simplification36 = Plane_Angle			# Angular_Velocity:1|Time:1
Simplification37 = Angular_Velocity		# Plane_Angle:1|Time:-1
Simplification38 = Angular_Velocity		# Angular_Acceleration:1|Time:1
Simplification39 = Angular_Acceleration	# Angular_Velocity:1|Time:-1
Simplification40 = Torsional_Angle		# Torsional_Velocity:1|Time:1
Simplification41 = Torsional_Velocity		# Torsional_Angle:1|Time:-1
Simplification42 = Torsional_Velocity		# Torsional_Acceleration:1|Time:1
Simplification43 = Torsional_Acceleration	# Torsional_Velocity:1|Time:-1
Simplification44 = Specific_Loudness		# Loudness:1|Frequency_Group:-1
Simplification45 = Frequency_Group			# Loudness:1|Specific_Loudness:-1
Simplification46 = Loudness				    # Specific_Loudness:1|Frequency_Group:1
; ----------------------------------------------------------------------
;			Correspondance unité TEDS <=> Grandeur OROS
; ----------------------------------------------------------------------
[TEDSUNITTOOROS]
Number = 60
Unit1=\"Nm/radian\"		(0,-1,0, 2,1,-2, 0,0,0,0,1,0)			#Force:1|Length:1|Plane_Angle:-1
Unit2=\"Nm\"				(0,-1,0, 2,1,-2, 0,0,0,0,1,0)			#Force:1|Length:1|Plane_Angle:-1
Unit3=\"oz-in\"			(0,-1,0, 2,1,-2, 0,0,0,0,0.00706155,0)	#Force:1|Length:1|Plane_Angle:-1
Unit4=\"V/(m/s²)\"		(0,0,0,1,1,-1,-1,0,0,0,1,0)				#Potential_Difference:1|Acceleration:-1
Unit5=\"radian\"			(0, 1,0, 0,0, 0, 0,0,0,0,1,0)			#Plane_Angle:1
Unit6=\"degrees\"			(0, 1,0, 0,0, 0, 0,0,0,0,0.0174533,0)	#Plane_Angle:1
Unit7=\"days\"			(0,0,0,0,0,1,0,0,0,0,86400,0)			#Time:1
Unit8=\"sec\"				(0, 0,0, 0,0, 1, 0,0,0,0,1,0)			#Time:1
Unit9=\"°C\"				(0, 0,0, 0,0, 0, 0,1,0,0,1,-273.15)		#Temperature_Kelvin:1
Unit10=\"Pa\"				(0, 0,0,-1,1,-2, 0,0,0,0,1,0)			#Accoustic_Pressure:1
Unit11=\"%\"				(1, 0,0, 0,0, 0, 0,0,0,0,100,0)			#Percentage:1
Unit12=\"PSI\"			(0, 0,0,-1,1,-2, 0,0,0,0,6894.757,0)	#Accoustic_Pressure:1
Unit13=\"Hz\"				(0, 0,0, 0,0,-1, 0,0,0,0,1,0)			#Frequency:1
Unit14=\"V\"				(0, 0,0, 2,1,-3,-1,0,0,0,1,0)			#Potential_Difference:1
Unit15=\"F\"				(0, 0,0,-2,-1,2,0,0,0,0,1,0)			#Temperature:1
Unit16=\"K\"				(0, 0,0, 0,0, 0, 0,1,0,0,1,0)			#Temperature:1
Unit17=\"m\"				(0, 0,0, 1,0, 0, 0,0,0,0,1,0)			#Length:1
Unit18=\"mm\"				(0, 0,0, 1,0, 0, 0,0,0,0,0.001,0)		#Length:1
Unit19=\"in\"				(0, 0,0, 1,0, 0, 0,0,0,0,0.0254,0)		#Length:1
Unit20=\"mph\"			(0, 0,0, 1,0,-1, 0,0,0,0,0.44704,0)		#Velocity:1
Unit21=\"m/s\"			(0, 0,0, 1,0,-1, 0,0,0,0,1,0)			#Velocity:1
Unit22=\"m/s²\"			(0, 0,0, 1,0,-2, 0,0,0,0,1,0)			#Acceleration:1
Unit23=\"ga\"				(0, 0,0, 1,0,-2, 0,0,0,0,9.80665,0)		#Acceleration:1
Unit24=\"A\"				(0, 0,0, 0,0, 0, 1,0,0,0,1,0)			#Intensity:1
Unit25=\"mA\"				(0, 0,0, 0,0, 0, 1,0,0,0,0.001,0)		#Intensity:1
Unit26=\"A rms\"			(0, 0,0, 0,0, 0, 1,0,0,0,1,0)			#Intensity:1
Unit27=\"W\"				(0, 0,0, 2,1,-3, 0,0,0,0,1,0)			#Power:1
Unit28=\"strain\"			(1, 0,0, 1,0, 0, 0,0,0,0,1,0)			#Strain:1
Unit29=\"microstrain\"	(1, 0,0, 1,0, 0, 0,0,0,0,1e-6,0)		#Strain:1
Unit30=\"N\"				(0, 0,0, 1,1,-2, 0,0,0,0,1,0)			#Force:1
Unit31=\"V rms\"			(0, 0,0, 2,1,-3,-1,0,0,0,1,0)			#Potential_Difference:1
Unit32=\"radian/s\"		(0, 1,0, 0,0,-1, 0,0,0,0,1,0)			#Angular_Velocity:1
Unit33=\"rpm\"			(0, 1,0, 0,0,-1, 0,0,0,0,0.104720,0)	#Angular_Velocity:1
Unit34=\"Ohm\"			(0, 0,0, 2,1,-3,-2,0,0,0,1,0)			#Resistance:1
Unit35=\"V/N\"			(0,0,0,1,0,-1,-1,0,0,0,1,0)				#Potential_Difference:1|Force:-1
Unit36=\"%/decade\"		(6,0,0,0,0,-1,0,0,0,0,0.01,0)			#Percentage:1|Time:1|Time:-1
Unit37=\"%/°C\"			(0,0,0,0,0,0,0,-1,0,0,0.01,0)			#Percentage:1|Temperature:-1
Unit38=\"N/m\"			(0,0,0,0,1,-2, 0,0,0,0,1,0)				#Force:1|Length:-1
Unit39=\"V/Pa\"			(0,0,0,3,0,-1,-1,0,0,0,1,0)				#Potential_Difference:1|Accoustic_Pressure:-1
Unit40=\"dB\"				(3,0,0,2,1,-3,-1,0,0,0,0.05,0)			#Undefined_Magnitude:1
Unit41=\"g\"				(0, 0,0, 0,1, 0, 0,0,0,0,0.001,0)		#Mass:1
Unit42=\"lb\"				(0, 0,0, 1,1,-2, 0,0,0,0,4.44822,0)		#Force:1
Unit43=\"kg\"				(0, 0,0, 0,1, 0, 0,0,0,0,1,0)			#Mass:1
Unit44=\"fps\"			(0, 0,0, 1,0,-1, 0,0,0,0,0.3048,0)		#Velocity:1
Unit45=\"kg/s\"			(0, 0,0, 0,1,-1, 0,0,0,0,1,0)			#Mass:1|Time:-1
Unit46=\"V/V\"			(1, 0,0, 2,1,-3,-1,0,0,0,1,0)			#Potential_Difference:1|Potential_Difference:-1
Unit47=\"mm²\"			(0, 0,0, 2,0, 0, 0,0,0,0,1E-6,0)		#Surface:1
Unit48=\"W/°C\"			(0,0,0,2,1,-3,0,-1,0,0,1,0)				#Power:1|Temperature:-1
Unit49=\"kgf\"			(0, 0,0, 1,1,-2, 0,0,0,0,9.80665,0)		#Force:1
Unit50=\"m³\"				(0,0,0,3,0,0,0,0,0,0,1,0)				#Volume:1
Unit51=\"kg/m³\"			(0, 0,0,-3,1, 0, 0,0,0,0,1,0)			#Mass:1|Volume:-1
Unit52=\"m³/m³\"			(1, 0,0, 3,0, 0, 0,0,0,0,1,0)			#Volume:1|Volume:-1
Unit53=\"l/l\"			(1, 0,0, 3,0, 0, 0,0,0,0,1,0)			#Volume:1|Volume:-1
Unit54=\"m³/hr			(0, 0,0, 3,0,-1, 0,0,0,0,3600,0)		#Volume:1|Time:-1
Unit55=\"gpm				(0, 0,0, 3,0,-1, 0,0,0,0,6.30902e-5,0)	#Volume:1|Time:-1
Unit56=\"cfm\"			(0, 0,0, 3,0,-1, 0,0,0,0,4.71947e-4,0)	#Volume:1|Time:-1
Unit57=\"l/min\"			(0, 0,0, 3,0,-1, 0,0,0,0,1.66667e-5,0)	#Volume:1|Time:-1
Unit58=\"RH\"				(1, 0,0,-3,1, 0, 0,0,0,0,1,0)			#Mass:1|Volume:-1|Mass:-1|Volume:1
Unit59=\"m³/s\"			(0, 0,0, 3,0,-1, 0,0,0,0,1,0)			#Volume:1|Time:-1
Unit60=\"g/l\"			(0, 0,0,-3,1, 0, 0,0,0,0,1,0)			#Mass:1|Volume:-1
"""