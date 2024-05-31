# ElGamal Cryptosystems on Elliptic Curves
Elliptic Curve Cryptography and Elliptic Curve Digital Signature redesigned by [Trần Quốc Việt Anh](https://github.com/VANH1810)

<div id="readme-top"></div>
<!-- TABLE OF CONTENTS -->

## Table of contents

<details>
  <ol>
    <li>
      <a href="#1-general-information">General Information</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#2-parameters">Parameters</a></li>
    <li>
      <a href="#3-getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#4-usage">Usage</a></li>
    <li><a href="#5-contributing">Contributing</a></li>
    <li><a href="#6-code-of-conduct">Code of Conduct</a></li>
    <li><a href="#7-funding">Funding</a></li>
    <li><a href="#8-license">License</a></li>
    <li><a href="#9-references">Reference</a></li>
    <li><a href="#10-contact">Contact</a></li>
  </ol>
</details>

<!-- GENAERAL INFORMATION -->
## 1. General Information

ElGamal Cryptosystems on Elliptic Curves and Elliptic Curve Digital Signature

This is an easy-to-use API implementation of Elgamal Encryption and Decryption using Elliptic Curve Cryptography, implemented purely in Python. 

Moreover, it helps in creating digital signatures and validating signatures.

You can create and use your own Elliptic curve using the [BuildECC](../BuildECC.py)

* Note: The Elliptic curve construction feature is not optimal, it only works with curves on Zp with small p and can run for a long time with large p. If you have an algorithm that helps build highways more optimally, I look forward to your contribution.

### Built With

[Python](https://www.python.org/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 2. Parameters
### [ElGamal Cryptosystems on Elliptic Curves](../ECC%20-%20Encrypt%20and%20Decrypt/)
* The elliptic curve domain parameters used are over Fp associated with a curve secp384r1.
* The parameters of the curve are written in [PublicKey](../ECC%20-%20Encrypt%20and%20Decrypt/publicKey.txt) or [secp384r1](../secp384r1.py)
* You can learn about this elliptic curve in the references section

### [Elliptic Curve Digital Signature](../ECDSA/)
* Elliptic curve I used:  y^2 = x^3 + 872338 * x + 842444
* Over Zp, p = 937151
* GenPoint: (16213, 331227)
* Number of points in the field [Order of G]: 937537
* Private Key: 562997
* Public Key: (295013, 729855)

## 3. Getting Started

### Prerequisites

This repository currently supports Window.
* You have to install Python 3.10.0 or higher. You should install Python in [Python](https://www.python.org/downloads/)

### Installation
1. Clone the repository to local computer

  ```bash
   git clone https://github.com/VANH1810/ElGamal-Cryptosystems-on-Elliptic-Curves.git
  ```
2. Check the Python version
  ```bash
   py --version
  ```
<p align="right">(<a href="#readme-top">Back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## 4. Usage
### [ElGamal Cryptosystems on Elliptic Curves](../ECC%20-%20Encrypt%20and%20Decrypt/)
#### Encryption
* Please write down the plaintext you want to encrypt [Plain text](../ECC%20-%20Encrypt%20and%20Decrypt/plainText.txt)
* To Encryption
  ``` ssh
    py Encrypt.py
    ```
* Then the ciphertext will be written in [Cipher text](../ECC%20-%20Encrypt%20and%20Decrypt/cipherText.txt)

#### Decryption
* Please write down the cipher text you want to decrypt [Cipher text](../ECC%20-%20Encrypt%20and%20Decrypt/cipherText.txt)

* To Decryption
  ``` ssh
    py Decrypt.py
    ```
* Then the Decrypted Text will be written in [Decrypted Text](../ECC%20-%20Encrypt%20and%20Decrypt/decryptedText.txt)

### [Elliptic Curve Digital Signature](../ECDSA/)
#### Sign
* Please write down the message you want to sign in [Message](../ECDSA/message.txt)
* To sign
  ``` ssh
      py Sign.py
* Then the signature will be written in [Signature](../ECDSA/signature.txt) 

#### Verify
* Please write down the message you want to verify in [Message](../ECDSA/message.txt) and the signature in [Signature](../ECDSA/signature.txt)
* To verify
  ``` ssh
      py Verify.py
  ```
* If signature is valid or invalid, the message will be printed to the screen

#### Other functions
* To Build a new Elliptic Curve
  ``` ssh
   py BuildECC.py
  ```
* To Generate a Prime
  ``` ssh
    py GeneratePrime.py
    ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## 5. Contributing

If you're interested in contributing to My project, we welcome your input. Whether you're a seasoned developer or just starting out, there are many ways you can help improve the project. You can contribute code, documentation, bug reports, or feature requests. To get started, check out the contributing guidelines in the [Contributing](CONTRIBUTING.md) file.

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CODE OF CONDUCT -->
## 6. Code of Conduct
We want everyone who participates in my project to feel welcome and respected. To ensure that happens, we've established a code of conduct that outlines our expectations for behavior. You can read the full text of the code of conduct in the [Code of Conduct](CODE_OF_CONDUCT.md) file.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- FUNDING -->
## 7. Funding
My project is currently self-funded and developed on a volunteer basis. If you're interested in supporting the project financially, we welcome your contributions. You can donate through our/my Open Collective page.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## 8. License
My project is released under the [MIT License](LICENSE.md). This means you're free to use, modify, and distribute the software for any purpose, including commercial use. However, we provide no warranties or guarantees, so use the software at your own risk.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- REFERENCES -->
## 9. References
* [Stinson Paterson_ Cryptography Theory And Practice - CRC Press (2019)](https://www.taylorfrancis.com/books/mono/10.1201/9781315282497/cryptography-douglas-robert-stinson-maura-paterson)
* [Elliptic Curve Digital Signature Algorithm](https://learnmeabitcoin.com/technical/cryptography/elliptic-curve/ecdsa/)
* [SEC 2: Recommended Elliptic Curve Domain Parameters](https://www.secg.org/sec2-v2.pdf)
* [ElGamal Cryptosystems on Koblitz curve secp256k1](https://github.com/Yash0day/ElgamalEncryption-using-ECC)
* [Tinyec Python Libarary](https://pypi.org/project/tinyec/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## 10. Contact

* My facebook: Tran Quoc Viet Anh - [quocvietanh.tran](https://www.facebook.com/quocvietanh.tran/) 
* Email: tqvabk24@gmail.com
*My github: [https://github.com/VANH1810](https://github.com/VANH1810)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
