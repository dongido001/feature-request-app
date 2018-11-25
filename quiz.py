from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABb-AboyasdiVTj1HALSo20qehU6eTak46s60_GEIRu3g06kAR5xnJ3qc6Ey-S4fUhe8-B4lGlbdQ2sBw-fXk8SnJBhqc7FWS0sWs1a63lonxwtBwBEQo4VS7iWKHd1YFdzdy444oC6HPs7yp6rpQJPDgfYe1YWimRjdoO09GoAYsg6z8TXG5TRD9-H4su6eon2xncy'

def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()