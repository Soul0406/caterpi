//Variables del Puerto Serial

//Motor 1
int ENA = 10;
int IN1 = 9;
int IN2 = 8;

//Motor 2
int ENB = 5;
int IN3 = 7;
int IN4 = 6;

//motobomba
int motobomba =11;
int led_verde =4;
int led_rojo =12;

void setup() {
  // Marcar pines como salidas
  pinMode (ENA, OUTPUT);
  pinMode (ENB, OUTPUT);
  pinMode (IN1, OUTPUT);
  pinMode (IN2, OUTPUT);
  pinMode (IN3, OUTPUT);
  pinMode (IN4, OUTPUT);
  pinMode (motobomba, OUTPUT);
  pinMode (led_verde, OUTPUT);
  pinMode (led_rojo, OUTPUT);

  digitalWrite (motobomba, HIGH);
  
  // Iniciar comunicación serial a 9600 bps
  Serial.begin(9600);
}

void Adelante ()
{
  //Direccion motor 1
  digitalWrite (IN1, HIGH);
  digitalWrite (IN2, LOW);
  analogWrite (ENA, 255);//Velocidad de motor 1
   //Direccion motor 2
  digitalWrite (IN3, HIGH);
  digitalWrite (IN4, LOW);
  analogWrite (ENB, 200);//Velocidad de motor 2
}

void Atras ()
{
  //Direccion motor 1
  digitalWrite (IN1, LOW);
  digitalWrite (IN2, HIGH);
  analogWrite (ENA, 200);//Velocidad de motor 1
   //Direccion motor 2
  digitalWrite (IN3, LOW);
  digitalWrite (IN4, HIGH);
  analogWrite (ENB, 200);//Velocidad de motor 2
}

void Derecha ()
{
  //Direccion motor 1
  digitalWrite (IN1, HIGH);
  digitalWrite (IN2, LOW);
  analogWrite (ENA, 200);//Velocidad de motor 1
   //Direccion motor 2
  digitalWrite (IN3, LOW);
  digitalWrite (IN4, HIGH);
  analogWrite (ENB, 100);//Velocidad de motor 2
}

void Izquierda ()
{
  //Direccion motor 1
  digitalWrite (IN1, LOW);
  digitalWrite (IN2, HIGH);
  analogWrite (ENA, 150);//Velocidad de motor 1
   //Direccion motor 2
  digitalWrite (IN3, HIGH);
  digitalWrite (IN4, LOW);
  analogWrite (ENB, 150);//Velocidad de motor 2
}
void Parar ()
{
  //Direccion motor 1
  digitalWrite (IN1, LOW);
  digitalWrite (IN2, LOW);
  analogWrite (ENA, 0);//Velocidad de motor 1
   //Direccion motor 2
  digitalWrite (IN3, LOW);
  digitalWrite (IN4, LOW);
  analogWrite (ENB, 0);//Velocidad de motor 2
}

void Motobomba_on(){
  digitalWrite (motobomba, LOW);
  digitalWrite (led_verde, HIGH);
  digitalWrite (led_rojo, LOW);
}

void Motobomba_off(){
  digitalWrite (motobomba, HIGH);
  digitalWrite (led_verde, LOW);
  digitalWrite (led_rojo, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
    if (Serial.available() > 0) {
    char comando = Serial.read();
    Serial.println(comando);
    
    switch (comando) {
      case 'F':
        Derecha();
        break;
      case 'B':
        Izquierda();
        break;
      case 'R':
        Adelante();
        break;
      case 'L':
        Atras();
        break;
      case 'S':
        Parar();
        break;
      case 'T':
        Motobomba_on();
        break;
      case 'N':
        Motobomba_off();
        break; 
    }
  }
}
