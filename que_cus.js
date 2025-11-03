// buyer.js

// รอให้ HTML โหลดเสร็จก่อน
document.addEventListener('DOMContentLoaded', () => {

    // 1. หาองค์ประกอบที่เราจะอัปเดต
    const statusCard = document.querySelector('.status-card');
    const statusTextElement = document.getElementById('status-text');
    
    // 1.1 ตรวจสอบว่าหาองค์ประกอบเจอไหม
    if (!statusCard || !statusTextElement) {
        console.error('ไม่พบการ์ดสถานะ (#status-text หรือ .status-card)');
        return; // หยุดทำงานถ้าหาไม่เจอ
    }
    
    // 1.2 ดึง ID ของออเดอร์จาก 'data-order-id' ที่เราควรจะใส่ไว้ใน HTML
    const orderId = statusCard.dataset.orderId;
    
    if (!orderId) {
        console.error('ไม่พบ data-order-id บน .status-card');
        return; // หยุดทำงานถ้าไม่มี orderId
    }

    let pollingInterval; // สร้างตัวแปร interval ไว้ข้างนอก

    // 2. ⭐️ ฟังก์ชันสำหรับเช็คสถานะ
    async function checkStatus() {
        console.log(`กำลังตรวจสอบสถานะออเดอร์: ${orderId}`);
        try {
            const response = await fetch(`/api/order/${orderId}/status`); // ส่ง GET
            
            if (!response.ok) {
                 throw new Error('Network response was not ok');
            }
            
            const data = await response.json();

            if (data.success) {
                // 3. ถ้าสถานะที่ได้คือ "complete"
                if (data.status === 'complete') {
                    statusTextElement.innerText = 'อาหารเสร็จแล้ว!';
                    statusTextElement.style.color = '#4CAF50'; // สีเขียว
                    statusTextElement.style.backgroundColor = '#f0fff0';
                    
                    // 4. ⭐️ หยุดถามซ้ำ (สำคัญมาก)
                    if (pollingInterval) {
                        clearInterval(pollingInterval); 
                    }
                } else {
                    // ถ้ายังเป็น 'pending' ก็ไม่ต้องทำอะไร
                    statusTextElement.innerText = 'กำลังเตรียมอาหาร...';
                }
            }
        } catch (error) {
            console.error('ไม่สามารถเช็คสถานะได้:', error);
            // (อาจจะต้องหยุด polling ถ้า error ถาวร)
        }
    }

    // 5. ⭐️ สั่งให้เช็คสถานะครั้งแรกทันที
    checkStatus();

    // 6. ⭐️ สั่งให้เช็คสถานะซ้ำๆ ทุก 5 วินาที (5000ms)
    pollingInterval = setInterval(checkStatus, 5000);
});