// seller.js

// รอให้ HTML โหลดเสร็จก่อน
document.addEventListener('DOMContentLoaded', () => {

    // 1. เลือกปุ่ม "เสร็จแล้ว" ทุกปุ่ม
    document.querySelectorAll('.btn-done').forEach(button => {
        
        button.addEventListener('click', async function(event) {
            
            // 2. หาการ์ดแม่ และดึง ID ของออเดอร์
            const orderCard = event.target.closest('.order-card');
            
            // (ในโค้ดจริง คุณควรใส่ data-id="101" ไว้ที่ .order-card)
            // แต่ตอนนี้เราจะดึงจาก H3 ที่เขียนว่า "คิวที่ #101"
            const orderIdText = orderCard.querySelector('h3').innerText; 
            const orderId = orderIdText.replace('คิวที่ #', ''); // ได้ "101"

            // ป้องกันการกดซ้ำ
            event.target.disabled = true;
            event.target.innerText = 'กำลังบันทึก...';

            try {
                // 3. ⭐️ ส่งคำขอ (POST) ไปยัง Flask Backend
                const response = await fetch(`/api/order/${orderId}/complete`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                if (!response.ok) {
                    throw new Error('Server ตอบกลับว่ามีปัญหา');
                }

                // 4. ⭐️ ถ้า Backend ตอบ OK (บันทึกสำเร็จ) ค่อยซ่อนการ์ด
                console.log(`ออเดอร์ ${orderId} บันทึกสำเร็จ!`);
                
                orderCard.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                orderCard.style.opacity = '0';
                orderCard.style.transform = 'scale(0.95)'; // เอฟเฟกต์ยุบลงเล็กน้อย

                setTimeout(() => {
                    orderCard.remove(); 
                }, 500); // 0.5 วินาที

            } catch (error) {
                // 5. ถ้าล้มเหลว ให้แจ้งเตือน และคืนค่าปุ่ม
                console.error('เกิดข้อผิดพลาด:', error);
                alert('ไม่สามารถอัปเดตสถานะได้ กรุณาลองใหม่');
                event.target.disabled = false;
                event.target.innerText = 'เสร็จแล้ว';
            }
        });
    });

});