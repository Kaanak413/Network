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

int connectcosts1[4] = { 1,  0,  1, 999 };

struct distance_table 
{
  int costs[4][4];
} dt1;


/* students to write the following two routines, and maybe some others */


rtinit1() 
{
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            dt1.costs[i][j] = 999;
        }
        dt1.costs[i][i] = connectcosts1[i];
    }
    struct rtpkt packet;
    packet.sourceid = 1;

    for (int i = 0; i < 4; i++) { // Only neighbors (ignore self-loop)
        if (i==packet.sourceid)
        {
            continue;
        }
        
        if (connectcosts1[i] < 999) {
            packet.destid = i;
            for (int j = 0; j < 4; j++) {
                packet.mincost[j] = dt1.costs[j][j]; // Minimum costs
            }
            tolayer2(packet);
        }
    }

}


rtupdate1(rcvdpkt)
  struct rtpkt *rcvdpkt;
  
{
    int source = rcvdpkt->sourceid;
    int updated = 0;

    // Update the distance table
    for (int i = 0; i < 4; i++) {
        int newCost = dt1.costs[1][source] + rcvdpkt->mincost[i];
        if (newCost < dt1.costs[1][i]) {
            dt1.costs[1][i] = newCost;
            updated = 1;
        }
    }
    if (updated) {
        struct rtpkt packet;
        packet.sourceid = 1;

        for (int i = 0; i < 4; i++) { // Only neighbors
            if (i==packet.sourceid)
            {
                continue;
            }
            if (dt1.costs[1][i] < 999) {
                packet.destid = i;
                for (int j = 0; j < 4; j++) {
                    packet.mincost[j] = dt1.costs[1][j]; // Updated min costs
                }
                tolayer2(packet);
            }
        }
    }

}


printdt1(dtptr)
  struct distance_table *dtptr;
  
{
  printf("             via   \n");
  printf("   D1 |    0     2 \n");
  printf("  ----|-----------\n");
  printf("     0|  %3d   %3d\n",dtptr->costs[0][0], dtptr->costs[0][2]);
  printf("dest 2|  %3d   %3d\n",dtptr->costs[2][0], dtptr->costs[2][2]);
  printf("     3|  %3d   %3d\n",dtptr->costs[3][0], dtptr->costs[3][2]);

}



linkhandler1(linkid, newcost)   
int linkid, newcost;   
/* called when cost from 1 to linkid changes from current value to newcost*/
/* You can leave this routine empty if you're an undergrad. If you want */
/* to use this routine, you'll need to change the value of the LINKCHANGE */
/* constant definition in prog3.c from 0 to 1 */
	
{
}

