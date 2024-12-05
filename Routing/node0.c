#include <stdio.h>

#define NUM_NODES 4
#define INFINITY 999

extern struct rtpkt {
    int sourceid;       /* id of sending router sending this pkt */
    int destid;         /* id of router to which pkt being sent */
    int mincost[NUM_NODES]; /* min cost to nodes 0 ... 3 */
};

extern int TRACE;
extern int YES;
extern int NO;

struct distance_table {
    int costs[NUM_NODES][NUM_NODES];
} dt0;

/* Function Prototypes */
void tolayer2(struct rtpkt packet);
void rtinit0();
void rtupdate0(struct rtpkt *rcvdpkt);

/* Initialize node 0 */
void rtinit0() {
    int directCosts[NUM_NODES] = {0, 1, 3, 7};

    // Initialize distance table
    for (int i = 0; i < NUM_NODES; i++) {
        for (int j = 0; j < NUM_NODES; j++) {
            dt0.costs[i][j] = INFINITY;
        }
        dt0.costs[i][i] = directCosts[i];
    }

    // Send initial packets to neighbors
    struct rtpkt packet;
    packet.sourceid = 0;

    for (int i = 1; i < NUM_NODES; i++) { // Only neighbors (ignore self-loop)
        if (directCosts[i] < INFINITY) {
            packet.destid = i;
            for (int j = 0; j < NUM_NODES; j++) {
                packet.mincost[j] = dt0.costs[j][j]; // Minimum costs
            }
            tolayer2(packet);
        }
    }
}

/* Update distance table based on received packet */
void rtupdate0(struct rtpkt *rcvdpkt) {
    int source = rcvdpkt->sourceid;
    int updated = 0;

    // Update the distance table
    for (int i = 0; i < NUM_NODES; i++) {
        int newCost = dt0.costs[0][source] + rcvdpkt->mincost[i];
        if (newCost < dt0.costs[0][i]) {
            dt0.costs[0][i] = newCost;
            updated = 1;
        }
    }

    // If table is updated, send new distance vector to neighbors
    if (updated) {
        struct rtpkt packet;
        packet.sourceid = 0;

        for (int i = 1; i < NUM_NODES; i++) { // Only neighbors
            if (dt0.costs[0][i] < INFINITY) {
                packet.destid = i;
                for (int j = 0; j < NUM_NODES; j++) {
                    packet.mincost[j] = dt0.costs[0][j]; // Updated min costs
                }
                tolayer2(packet);
            }
        }
    }
}

/* Print the distance table for node 0 */
printdt0(dtptr)
  struct distance_table *dtptr;
  
{
  printf("                via     \n");
  printf("   D0 |    1     2    3 \n");
  printf("  ----|-----------------\n");
  printf("     1|  %3d   %3d   %3d\n",dtptr->costs[1][1],
	 dtptr->costs[1][2],dtptr->costs[1][3]);
  printf("dest 2|  %3d   %3d   %3d\n",dtptr->costs[2][1],
	 dtptr->costs[2][2],dtptr->costs[2][3]);
  printf("     3|  %3d   %3d   %3d\n",dtptr->costs[3][1],
	 dtptr->costs[3][2],dtptr->costs[3][3]);
}

linkhandler0(linkid, newcost)   
  int linkid, newcost;

/* called when cost from 0 to linkid changes from current value to newcost*/
/* You can leave this routine empty if you're an undergrad. If you want */
/* to use this routine, you'll need to change the value of the LINKCHANGE */
/* constant definition in prog3.c from 0 to 1 */
	
{
}
