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
int connectcosts2[4] = { 3,  1,  0, 2 };

struct distance_table 
{
  int costs[4][4];
} dt2;


/* students to write the following two routines, and maybe some others */

void rtinit2() 
{
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            dt2.costs[i][j] = 999;
        }
        dt2.costs[i][i] = connectcosts2[i];
    }
    struct rtpkt packet;
    packet.sourceid = 2;

    for (int i = 0; i < 4; i++) { // Only neighbors (ignore self-loop)
        if (i==packet.sourceid)
        {
            continue;
        }
        
        if (connectcosts2[i] < 999) {
            packet.destid = i;
            for (int j = 0; j < 4; j++) {
                packet.mincost[j] = dt2.costs[j][j]; // Minimum costs
            }
            tolayer2(packet);
        }
    }

}


void rtupdate2(rcvdpkt)
  struct rtpkt *rcvdpkt;
  
{
    int source = rcvdpkt->sourceid;
    int updated = 0;

    // Update the distance table
    for (int i = 0; i < 4; i++) {
        int newCost = dt2.costs[2][source] + rcvdpkt->mincost[i];
        if (newCost < dt2.costs[2][i]) {
            dt2.costs[2][i] = newCost;
            updated = 1;
        }
    }
    if (updated) {
        struct rtpkt packet;
        packet.sourceid = 2;

        for (int i = 0; i < 4; i++) { // Only neighbors
            if (i==packet.sourceid)
            {
                continue;
            }
            if (dt2.costs[2][i] < 999) {
                packet.destid = i;
                for (int j = 0; j < 4; j++) {
                    packet.mincost[j] = dt2.costs[2][j]; // Updated min costs
                }
                tolayer2(packet);
            }
        }
    }
}


printdt2(dtptr)
  struct distance_table *dtptr;
  
{
  printf("                via     \n");
  printf("   D2 |    0     1    3 \n");
  printf("  ----|-----------------\n");
  printf("     0|  %3d   %3d   %3d\n",dtptr->costs[0][0],
	 dtptr->costs[0][1],dtptr->costs[0][3]);
  printf("dest 1|  %3d   %3d   %3d\n",dtptr->costs[1][0],
	 dtptr->costs[1][1],dtptr->costs[1][3]);
  printf("     3|  %3d   %3d   %3d\n",dtptr->costs[3][0],
	 dtptr->costs[3][1],dtptr->costs[3][3]);
}






