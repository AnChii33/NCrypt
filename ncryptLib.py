# Ncrypt v1.0

import random as rdn
import cipherFunc as cF
import listReader as lR
import hashlib as hb
import pymongo

class Ncrypt:

    # ------------------- ENCRYPTION FUNCTIONS -----------------

    class E:

        # main N-way encryption function
        def encrypt(dfile: str, n: int, mongoConnectURL: str) -> list:    
            keys = []         
            hashes = []      
            key = ""                     
            for _ in range(n+1):
                key = Ncrypt.E.cipherData(dfile, key)
                dHash = Ncrypt.E.hashCipheredData(dfile)    
                keys.append(key)
                hashes.append(dHash)
            
            entryCode = Ncrypt.E.storeCipheredData(dfile, key, mongoConnectURL)
            Ncrypt.E.storeHash(entryCode, hashes)

            return keys

        # load the cipher dictionary file
        def loadCipher() -> list:  
            cipherBook = []                        
            lR.readtolist(cipherBook, "cipher.txt")
            return rdn.choice(cipherBook)

        # cipher Data
        def cipherData(dfile: str, lastKey: int) -> int:                       
            cf = Ncrypt.E.loadCipher()
            cKey = cF.calculateKey(cf)
            validBit = 30 - sum([int(i) for i in str(cKey)])
            key = int(str(cKey) + str(validBit))

            while key == lastKey:
                cf = Ncrypt.E.loadCipher()
                cKey = cF.calculateKey(cf)
                validBit = 30 - sum([int(i) for i in str(cKey)])
                key = int(str(cKey) + str(validBit))
            else:
                data = []
                with open(dfile) as f:
                    data = f.readlines()
                for i in range(len(data)):
                    li = list(data[i])
                    for j in range(len(li)):
                        idx = ord(li[j]) - 33
                        if (idx >= 0) and (idx < 127):
                            li[j] = chr(cf[idx])
                    data[i] = "".join(li)
                
                with open(dfile, "w") as f:
                    f.writelines(data)
                
            return key
            

        # hash the ciphered data
        def hashCipheredData(dfile: str) -> str:
            x = ""
            with open(dfile) as f:
                x = f.read()
            hashX = hb.sha256(x.encode()).hexdigest()
            return hashX

        # store the ciphered data in database
        def storeCipheredData(dfile: str, key: int, mongoConnectURL) -> str:
            client = pymongo.MongoClient(mongoConnectURL)
            db = client["Ncrypt"]
            collection = db["DataStore"]
            x = ""
            with open(dfile) as f:
                x = f.read()
            with open(dfile, "w") as f:
                f.write("THIS FILE IS ENCRYPTED\n")

            collection.insert_one({"fKey":key, "data":x})
            entryCode = collection.find_one({"fKey":key}, {"fKey":0, "data":0, "_id":1})
            return str(entryCode["_id"])
            

        # store the hash
        def storeHash(entryCode: str, hashList: list):
            with open("logbook.txt", "a") as f:
                f.write(entryCode+" ")
                for i in hashList:
                    f.write(i+" ")
                f.write("\n")


    # ------------------- DECRYPTION FUNCTIONS -----------------

    class D:

        def decrypt(dfile: str, n: int, keyList: list, mongoConnectURL: str):
            fKey = keyList.pop(0)
            dataDict = Ncrypt.D.retriveCipheredData(fKey, mongoConnectURL)
            id = dataDict["_id"]
            entryCode = str(id)
            hashList = Ncrypt.D.retriveHash(entryCode)
            cText = str(dataDict["data"])

            validData = Ncrypt.D.matchHash(cText, hashList.pop())
            if validData:
                cText = Ncrypt.D.decipherData(fKey, cText)
            else:
                return None
            
            for i in range(n):
                validData = Ncrypt.D.matchHash(cText, hashList.pop())
                if validData:
                    ckey = keyList.pop(0)
                    try:
                        cText = Ncrypt.D.decipherData(ckey, cText)
                    except:
                        return None
                    
            with open(dfile, "w") as f:
                f.write(cText)

            with open("logbook.txt", "w+") as f:
                hashRec = f.readlines()
                for i in hashRec:
                    if i.find(entryCode) != -1:
                        hashRec.remove(i)
                f.writelines(hashRec)
            
            client = pymongo.MongoClient(mongoConnectURL)
            db = client["Ncrypt"]
            collection = db["DataStore"]
            collection.find_one_and_delete({"_id":id})
            
            print("SUCCESSFULLY DECRYPTED!")
            
                    





        def retriveCipheredData(fKey: int, mongoConnectURL: str) -> dict:
            client = pymongo.MongoClient(mongoConnectURL)
            db = client["Ncrypt"]
            collection = db["DataStore"]
            dataDict = collection.find_one({"fKey":fKey})
            return dataDict
        
        def retriveHash(entryCode: str) -> list:
            entries = []
            hashList = []
            with open("logbook.txt") as f:
                entries = f.readlines()
            entries = [i.split(" ") for i in entries]
            for i in entries:
                if i[0] == entryCode:
                    hashList = i[1:-1]
            return hashList
        
        def matchHash(cText: str, cHash: str) -> bool:
            x = hb.sha256(cText.encode()).hexdigest()
            if x == cHash:
                return True
            return False
        
        def keyValid(ckey: int) -> bool:
            ckey = list(str(ckey))
            if len(ckey) < 9:
                return False
            validBit = int(ckey.pop())
            if (30 - sum([int(i) for i in ckey])) == validBit:
                return True
            return False
        
        def identifyCipher(ckey: int) -> list:
            if Ncrypt.D.keyValid(ckey):
                ckey = ckey // 10
                cipherBook = []                        
                lR.readtolist(cipherBook, "cipher.txt")
                for i in cipherBook:
                    if cF.calculateKey(i) == ckey:
                        return i
                return None
            return None
        
        def decipherData(ckey: int, cText: str) -> str:
            cipher = Ncrypt.D.identifyCipher(ckey)
            if cipher:
                cText = list(cText)
                for i in range(len(cText)):
                    if ord(cText[i]) in cipher:
                        cText[i] = chr(cipher.index(ord(cText[i]))+33)
                cText = "".join(cText)
                return cText
            return None




if __name__ == "__main__":
    # Ncrypt.E.encrypt("cipherTest2.txt", 4, "mongodb://localhost:27017")

    Ncrypt.D.decrypt("cipherTest2.txt", 4, 111489240, "mongodb://localhost:27017")