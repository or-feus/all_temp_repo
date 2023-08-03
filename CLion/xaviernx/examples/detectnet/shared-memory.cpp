#include "function.hpp"

void CSharedMemroy::setShmId( int id )
{
    m_shmid = id;
}
 
 
void CSharedMemroy::setKey( key_t key )
{
    m_key = key;
}
 
 
void CSharedMemroy::setupSharedMemory( int size )
{
   // Setup shared memory, 11 is the size
 
   if ( ( m_shmid = shmget(m_key, size , IPC_CREAT | 0666)) < 0 )
   {
      printf("Error getting shared memory id");
      exit( 1 );
   }
}
 
 
void CSharedMemroy::attachSharedMemory()
{
   // Attached shared memory
   if ( ( *m_shared_memory = (char *)shmat( m_shmid , NULL , 0 ) ) == (char *)-1)
   {
      printf("Error attaching shared memory id");
      exit(1);
   }
}
 

void CSharedMemroy::copyToSharedMemory(unsigned int det_code)
{
    unsigned int *det_code_ptr = &det_code;
   // copy string to shared memory
   memcpy( *m_shared_memory, det_code_ptr , 1 );
//    sleep( 10 );
}
 
//void CSharedMemroy::close()
//{
//    sleep(10);
 
//   // Detach and remove shared memory
//   shmdt( (char *)m_shmid );
//   shmctl( m_shmid , IPC_RMID, NULL );
 
//}
 
