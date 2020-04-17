void setup() {
  // put your setup code here, to run once:
  pinMode(13,OUTPUT);
  digitalWrite(13,LOW);
  Serial.begin(9600);
  
  

}

void loop() {
  // put your main code here, to run repeatedly:
 if (Serial.available() > 0){
  if (Serial.read()== '1'){
    digitalWrite(13,HIGH);
    delay(15);
  }
  
 }
 else {
  digitalWrite(13,LOW);
 }
 
}
