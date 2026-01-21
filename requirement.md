# ASSIGNMENT 01  
**COURSE:** SOFTWARE ARCHITECTURE AND DESIGN

---

## 1. Objectives

• Understand Monolithic, Clean Architecture, and Microservices.  

• Design software systems using UML.  

• Implement Django + MySQL systems following three architectural styles.

---

## 2. Project Topic

Book Store Web System

---

## 3. Entities

Customer: id, name, email, password.  

Book: id, title, author, price, stock.  

Cart: id, customer_id, created_at.  

CartItem: id, cart_id, book_id, quantity.

---

## 4. Functional Requirements

• Customer registration and login.  

• View book catalog.  

• Add books to the shopping cart.  

• View shopping cart contents.

---

## 5. UML Design Requirements

Design the system using Visual Paradigm:

• Class Diagram  

• MVC Layer Diagram (Monolithic version)  

• Clean Architecture Diagram  

• Microservices Architecture Diagram  

Export diagrams as images or PDF files.

---

1

---

## 6. Implementation Requirements

### Version A – Monolithic Django

• Single Django project  

• Apps: accounts, books, cart  

• MySQL database

---

### Version B – Clean Architecture Django

Suggested project structure:

**Listing 1: Clean Architecture layout of the Django system**

project/

domain/
usecases/
interfaces/
infrastructure/
framework/ (Django)


---

### Version C – Microservices Django

The system is decomposed into independent services communicating via REST APIs:

• customer-service  

• book-service  

• cart-service

---

## 7. Database

• Use MySQL as the database system.  

• Each version maintains its own database.  

• Provide SQL scripts for table creation.

---

## 8. Submission

Submit the following:

• GitHub repository containing:

– /monolith  
– /clean  
– /micro  

• PDF report  

• UML design files

---

2

---

## 9. Deadline

Submission at the beginning of Week 2.

---

## 10. Grading Criteria

Item | Weight  
-----|-------
Correct UML design | 30%  
Working Monolithic version | 20%  
Correct Clean Architecture structure | 20%  
Working Microservices communication | 20%  
Report and on-time submission | 10%

---

## 11. Regulations

• ChatGPT is allowed as a support tool.  

• Students must understand submitted code.  

• Late submission will be penalized.

---

Good luck and enjoy building your system!

---
