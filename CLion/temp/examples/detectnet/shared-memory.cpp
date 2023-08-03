#include "function.hpp"

void CSharedMemory::setShmId(int id) {
    m_shmid = id;
}


void CSharedMemory::setKey(key_t key) {
    m_key = key;
}


void CSharedMemory::setupSharedMemory(int size) {
    // Setup shared memory, 11 is the size

    if ((m_shmid = shmget(m_key, size, IPC_CREAT | 0666)) < 0) {
        printf("Error getting shared memory id");
        exit(1);
    }
}


void CSharedMemory::attachSharedMemory() {
    // Attached shared memory
    if ((*m_shared_memory = (char *) shmat(m_shmid, NULL, 0)) == (char *) -1) {
        printf("Error attaching shared memory id");
        exit(1);
    }
}


void CSharedMemory::copyToSharedMemory(unsigned char totalframe, unsigned char det_code) {
    unsigned char value[2] = {0, 0};
    value[0] = totalframe;
    value[1] = det_code;
    // copy string to shared memory
    memcpy(*m_shared_memory, value, 2);
//    sleep( 10 );
}

//void CSharedMemory::close()
//{
//    sleep(10);

//   // Detach and remove shared memory
//   shmdt( (char *)m_shmid );
//   shmctl( m_shmid , IPC_RMID, NULL );

//}
 

