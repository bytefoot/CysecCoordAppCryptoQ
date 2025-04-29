# **Cryptographic Challenge for Coordinator Applicants**  
*Prove your technical mastery and problem-solving skills*  

This simulated cryptanalysis task recreates real-world vulnerabilities our team exploited to place 7th internationally in eCTF 2023. Your mission: reverse-engineer our custom protocol by studying app.py and craft precision attacks to extract hidden flags.

## **Task 1: Broken Message Protocol**  
*A production system leaked this encrypted frame. Extract the hidden flag.*  

### Provided Data  
**Valid Frame (Hex):**  
```
d74b31d112f54559e6f81a5ba0c6ec05831103bc512818ae07435344057f181bd6fa6043f7f0dda07c3f8b5077268a5b812d2f81f0cdb88045bbfd5d5a8b1c69ad2a7d5959695c77af32a9322f5f072df0e201d767ff8d218ee370f8f7fd113acf5d800dc8d7d4f6ae6e7ec686f4c64d
```  

**Flag-Containing Frame (Hex):**  
```
3dcc8444d4a311503406ded82146e47b73d5c294da3f143022e6098faa4298382b33a8c5ecf3cea51ec5a5d68a1020d6651af274c1a18e5e0784980418ed0f5898531bfc8769581c2a2fef3847481996d84ea83d93991e6be28e5f789dbd97a8629a4b7725d33a651cf1c95c70083526
```  

## **Task 2: Dual-Layer Encryption**  
*Analyze this twice-encrypted payload.*  

### Provided Data  
**Valid Frame (Hex):**  
```
106c25c2e18cac80b78f74918e0c54b7bb9422433a1665c958d8881a69a8c4275b9ecf3e2edbf892caa28eaf84c759656bbebd5efb8e139c22dd930f71fff9f8
```  

**Flag-Containing Frame (Hex):**  
```
93774b6fd89616fdbdab637bb390eef5dbe9b0746d5667c3e48487d0ec731b47e8e2e62c2e69c126be77d6f4fed586d1d5585ea174b54d1f4d6f5b1ec40ee7df
```  

## **Submission**  
```bash
# Submit your modified frames via:
curl -X POST https://1wymyen3v6.execute-api.eu-north-1.amazonaws.com/Prod/%7Bproxy+%7D/task{1|2} -H "Content-Type: application/json" -d '{"frame":"HEX_DATA"}'
```  

**Contact for clarifications:**  
Kevin Kinsey (CySec Strategist)  
📧 ep23b027@smail.iitm.ac.in | 📞 +91 6366577373  
