// Pin tanımlamaları
const int ledGPin = 13;
const int ledRPin = 10;

void setup() {
  // Seri haberleşme başlatılıyor
  Serial.begin(9600);

  // Pin modları ayarlanıyor
  pinMode(ledGPin, OUTPUT);
  pinMode(ledRPin, OUTPUT);

  // Başlangıçta LED'ler söndürülüyor
  digitalWrite(ledGPin, LOW);
  digitalWrite(ledRPin, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    // Seri porttan gelen veriyi okuyoruz
    char receivedChar = Serial.read();

    // G harfi kontrolü
    if (receivedChar == 'G') {
      digitalWrite(ledGPin, HIGH);  // 13. pindeki LED'i yak
      digitalWrite(ledRPin, LOW);   // 12. pindeki LED'i söndür
    }

    // R harfi kontrolü
    if (receivedChar == 'R') {
      digitalWrite(ledGPin, LOW);   // 13. pindeki LED'i söndür
      digitalWrite(ledRPin, HIGH);  // 12. pindeki LED'i yak
    }
  }
}
