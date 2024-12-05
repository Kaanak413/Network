#include <stdio.h>

extern struct rtpkt {
  int sourceid;       /* id of sending router sending this pkt */
  int destid;         /* id of router to which pkt being sent 
                         (must be an immediate neighbor) */
  int mincost[4];    /* min cost to node 0 ... 3 */
  };

extern int TRACE;
extern int YES;
extern int NO;
int connectcosts3[4] = { 7,  999,  2, 0 };

struct distance_table 
{
  int costs[4][4];
} dt3;

/* students to write the following two routines, and maybe some others */

void rtinit3() 
{
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            dt3.costs[i][j] = 999;
        }
        dt3.costs[i][i] = connectcosts3[i];
    }
    struct rtpkt packet;
    packet.sourceid = 3;

    for (int i = 0; i < 4; i++) { // Only neighbors (ignore self-loop)
        if (i==packet.sourceid)
        {
            continue;
        }
        
        if (connectcosts3[i] < 999) {
            packet.destid = i;
            for (int j = 0; j < 4; j++) {
                packet.mincost[j] = dt3.costs[j][j]; // Minimum costs
            }
            tolayer2(packet);
        }
    }
}


void rtupdate3(rcvdpkt)
  struct rtpkt *rcvdpkt;
  
{
    int source = rcvdpkt->sourceid;
    int updated = 0;

    // Update the distance table
    for (int i = 0; i < 4; i++) {
        int newCost = dt3.costs[3][source] + rcvdpkt->mincost[i];
        if (newCost < dt3.costs[3][i]) {
            dt3.costs[3][i] = newCost;
            updated = 1;
        }
    }
    if (updated) {
        struct rtpkt packet;
        packet.sourceid = 3;

        for (int i = 0; i < 4; i++) { // Only neighbors
            if (i==packet.sourceid)
            {
                continue;
            }
            if (dt3.costs[3][i] < 999) {
                packet.destid = i;
                for (int j = 0; j < 4; j++) {
                    packet.mincost[j] = dt3.costs[3][j]; // Updated min costs
                }
                tolayer2(packet);
            }
        }
    }
}


printdt3(dtptr)
  struct distance_table *dtptr;
  
{
  printf("             via     \n");
  printf("   D3 |    0     2 \n");
  printf("  ----|-----------\n");
  printf("     0|  %3d   %3d\n",dtptr->costs[0][0], dtptr->costs[0][2]);
  printf("dest 1|  %3d   %3d\n",dtptr->costs[1][0], dtptr->costs[1][2]);
  printf("     2|  %3d   %3d\n",dtptr->costs[2][0], dtptr->costs[2][2]);

}






