## Regular Expression to NFA
<Br>

#### จัดทำโดย

##### นาย กิตติกานต์ มากผล 6410450087
##### นาย นิสิต นะมิตร 6410451148
##### นาย พีรสิษฐ์ พลอยอร่าม 6410451237
##### นาย ศิวกร ภาสว่าง 6410451423
<br>
<br>


## Operation
- #### u for Union
- #### . for Concat
- #### \* for Kleene
- #### ( ) for Parentheses
## Run Program
#### Run Command
``` Bash
# Run Defaults
python3 main.py

#input Regex
aub
```

#### Output
``` Bash
# Print NFA Table Transitions
Recieve: aub
NFA define by:
 --------------------------------------
| States |         Transitions         |
|        |    E    |    a    |    b    |
|--------|------------------------------
|   Q1   | Q2 Q3
|--------|---------|---------|---------|
|   Q2   |            Q4
|--------|---------|---------|---------|
|   Q3   |                       Q6
|--------|---------|---------|---------|
|   Q4   | Q5
|--------|---------|---------|---------|
|   Q5   |
|--------|---------|---------|---------|
|   Q6   | Q5
|--------|---------|---------|---------|

Start state is: Q1
Final states is: Q5
```

<br>
<br>

#### Run Command With Option
```Bash
python3 main.py [option]
```
-o, --out สำหรับบันทึก NFA Table Transitions เป็น File Json

``` Bash
# Run With argument
python3 main.py --out

#input Regex
(aub)*aab
```
#### Output
``` Bash
# Print NFA Table Transitions
(aub)*aab

Recieve: (aub)*aab
NFA define by:
 --------------------------------------
| States |         Transitions         |
|        |    E    |    a    |    b    |
|--------|------------------------------
|   Q1   | Q2 Q3
|--------|---------|---------|---------|
|   Q2   | Q4 Q5
|--------|---------|---------|---------|
|   Q3   | Q8
|--------|---------|---------|---------|
|   Q4   |            Q6
|--------|---------|---------|---------|
|   Q5   |                       Q14
|--------|---------|---------|---------|
|   Q6   | Q7
|--------|---------|---------|---------|
|   Q7   | Q2 Q3
|--------|---------|---------|---------|
|   Q8   |            Q9
|--------|---------|---------|---------|
|   Q9   | Q10
|--------|---------|---------|---------|
|   Q10  |            Q11
|--------|---------|---------|---------|
|   Q11  | Q12
|--------|---------|---------|---------|
|   Q12  |                       Q13
|--------|---------|---------|---------|
|   Q13  |
|--------|---------|---------|---------|
|   Q14  | Q7
|--------|---------|---------|---------|

Start state is: Q1
Final states is: Q13

NFA Json Name [NFA_(aub)*aab.json] has been save.
```

#### File NFA Json
- Save at Directory output
- format name [ NFA_Regex.json ]