void setup() {
  // serial haberleşmeyi 9600baud kuruyoruz
  Serial.begin(9600);
 
  // pin 9,10u output olarak tanımla
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
}
 
void loop() {
  // gelen veri var mı kontrol ediyoruz
  if (Serial.available() > 0) {
    // gelen veriyi okutuyoruz
    String veri = Serial.readString();
 
    // eğer serialden gelen yazı green ise pin 9 u yüksek pin10u düşük yap
    if (veri == "Green") {
      digitalWrite(9, HIGH);
      digitalWrite(10, LOW);
    }
    // eğer serialden gelen yazı red ise pin 10 u yüksek pin9u düşük yap
    else if (veri == "Red") {
      digitalWrite(10, HIGH);
      digitalWrite(9, LOW);
    }
  }
}
