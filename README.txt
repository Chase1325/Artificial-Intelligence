Chase St. Laurent
CS 534 AI Project/HW 1 (Search Methods)

TO RUN THE CODE:
1. Ensure you have Python 3 installed
2. Ensure you have "python" set to Python3 environment variable
3. Navigate to the project directory
4. type into command line "python Search.py graph.txt"

	The format is: python Search.py <graph_file_txt>

	There are nine search algorithms which all run, outputs abbreviated as follows:
		DFS (Depth 1st Search)
		BFS (Breadth 1st Search)
		DLS (Depth Limited Search: Limit = 2)
		IDS (Iterative Deepening Search: All iterations shown)
		UCS (Uniform Cost Search)
		GS  (Greedy Search)
		ASS (A* or Astar Search)
		HC  (Hill-Climbing without Backtracking)
		BS  (Beam Search: Width = 2)

************************************************************************************************************
**************************************OUTPUT FROM "graph.txt"***********************************************
************************************************************************************************************
*DFS:
       Expanded      Queue
          S          [<S>]
          A          [<A,S> <D,S>]
          B          [<B,A,S> <D,A,S> <D,S>]
          C          [<C,B,A,S> <E,B,A,S> <D,A,S> <D,S>]
          E          [<E,B,A,S> <D,A,S> <D,S>]
          D          [<D,E,B,A,S> <F,E,B,A,S> <D,A,S> <D,S>]
          F          [<F,E,B,A,S> <D,A,S> <D,S>]
          G          [<G,F,E,B,A,S> <D,A,S> <D,S>]
Goal reached!

*BFS:
       Expanded      Queue
          S          [<S>]
          A          [<A,S> <D,S>]
          D          [<D,S> <B,A,S> <D,A,S>]
          B          [<B,A,S> <D,A,S> <A,D,S> <E,D,S>]
          D          [<D,A,S> <A,D,S> <E,D,S> <C,B,A,S> <E,B,A,S>]
          A          [<A,D,S> <E,D,S> <C,B,A,S> <E,B,A,S> <E,D,A,S>]
          E          [<E,D,S> <C,B,A,S> <E,B,A,S> <E,D,A,S> <B,A,D,S>]
          C          [<C,B,A,S> <E,B,A,S> <E,D,A,S> <B,A,D,S> <B,E,D,S> <F,E,D,S>]
          E          [<E,B,A,S> <E,D,A,S> <B,A,D,S> <B,E,D,S> <F,E,D,S>]
          E          [<E,D,A,S> <B,A,D,S> <B,E,D,S> <F,E,D,S> <D,E,B,A,S> <F,E,B,A,S>]
          B          [<B,A,D,S> <B,E,D,S> <F,E,D,S> <D,E,B,A,S> <F,E,B,A,S> <B,E,D,A,S> <F,E,D,A,S>]
          B          [<B,E,D,S> <F,E,D,S> <D,E,B,A,S> <F,E,B,A,S> <B,E,D,A,S> <F,E,D,A,S> <C,B,A,D,S> <E,B,A,D,S>]
          F          [<F,E,D,S> <D,E,B,A,S> <F,E,B,A,S> <B,E,D,A,S> <F,E,D,A,S> <C,B,A,D,S> <E,B,A,D,S> <A,B,E,D,S> <C,B,E,D,S>]
          D          [<D,E,B,A,S> <F,E,B,A,S> <B,E,D,A,S> <F,E,D,A,S> <C,B,A,D,S> <E,B,A,D,S> <A,B,E,D,S> <C,B,E,D,S> <G,F,E,D,S>]
          F          [<F,E,B,A,S> <B,E,D,A,S> <F,E,D,A,S> <C,B,A,D,S> <E,B,A,D,S> <A,B,E,D,S> <C,B,E,D,S> <G,F,E,D,S>]
          B          [<B,E,D,A,S> <F,E,D,A,S> <C,B,A,D,S> <E,B,A,D,S> <A,B,E,D,S> <C,B,E,D,S> <G,F,E,D,S> <G,F,E,B,A,S>]
          F          [<F,E,D,A,S> <C,B,A,D,S> <E,B,A,D,S> <A,B,E,D,S> <C,B,E,D,S> <G,F,E,D,S> <G,F,E,B,A,S> <C,B,E,D,A,S>]
          C          [<C,B,A,D,S> <E,B,A,D,S> <A,B,E,D,S> <C,B,E,D,S> <G,F,E,D,S> <G,F,E,B,A,S> <C,B,E,D,A,S> <G,F,E,D,A,S>]
          E          [<E,B,A,D,S> <A,B,E,D,S> <C,B,E,D,S> <G,F,E,D,S> <G,F,E,B,A,S> <C,B,E,D,A,S> <G,F,E,D,A,S>]
          A          [<A,B,E,D,S> <C,B,E,D,S> <G,F,E,D,S> <G,F,E,B,A,S> <C,B,E,D,A,S> <G,F,E,D,A,S> <F,E,B,A,D,S>]
          C          [<C,B,E,D,S> <G,F,E,D,S> <G,F,E,B,A,S> <C,B,E,D,A,S> <G,F,E,D,A,S> <F,E,B,A,D,S>]
          G          [<G,F,E,D,S> <G,F,E,B,A,S> <C,B,E,D,A,S> <G,F,E,D,A,S> <F,E,B,A,D,S>]
Goal reached!

*DLS:
       Expanded      Queue
          S          [<S>]
          A          [<A,S> <D,S>]
          B          [<B,A,S> <D,A,S> <D,S>]
          D          [<D,A,S> <D,S>]
          D          [<D,S>]
          A          [<A,D,S> <E,D,S>]
          E          [<E,D,S>]
Path not found :(

*IDS:
       Expanded      Queue

L=0       S          [<S>]

L=1       S          [<S>]
          A          [<A,S> <D,S>]
          D          [<D,S>]

L=2       S          [<S>]
          A          [<A,S> <D,S>]
          B          [<B,A,S> <D,A,S> <D,S>]
          D          [<D,A,S> <D,S>]
          D          [<D,S>]
          A          [<A,D,S> <E,D,S>]
          E          [<E,D,S>]

L=3       S          [<S>]
          A          [<A,S> <D,S>]
          B          [<B,A,S> <D,A,S> <D,S>]
          C          [<C,B,A,S> <E,B,A,S> <D,A,S> <D,S>]
          E          [<E,B,A,S> <D,A,S> <D,S>]
          D          [<D,A,S> <D,S>]
          E          [<E,D,A,S> <D,S>]
          D          [<D,S>]
          A          [<A,D,S> <E,D,S>]
          B          [<B,A,D,S> <E,D,S>]
          E          [<E,D,S>]
          B          [<B,E,D,S> <F,E,D,S>]
          F          [<F,E,D,S>]

L=4       S          [<S>]
          A          [<A,S> <D,S>]
          B          [<B,A,S> <D,A,S> <D,S>]
          C          [<C,B,A,S> <E,B,A,S> <D,A,S> <D,S>]
          E          [<E,B,A,S> <D,A,S> <D,S>]
          D          [<D,E,B,A,S> <F,E,B,A,S> <D,A,S> <D,S>]
          F          [<F,E,B,A,S> <D,A,S> <D,S>]
          D          [<D,A,S> <D,S>]
          E          [<E,D,A,S> <D,S>]
          B          [<B,E,D,A,S> <F,E,D,A,S> <D,S>]
          F          [<F,E,D,A,S> <D,S>]
          D          [<D,S>]
          A          [<A,D,S> <E,D,S>]
          B          [<B,A,D,S> <E,D,S>]
          C          [<C,B,A,D,S> <E,B,A,D,S> <E,D,S>]
          E          [<E,B,A,D,S> <E,D,S>]
          E          [<E,D,S>]
          B          [<B,E,D,S> <F,E,D,S>]
          A          [<A,B,E,D,S> <C,B,E,D,S> <F,E,D,S>]
          C          [<C,B,E,D,S> <F,E,D,S>]
          F          [<F,E,D,S>]
          G          [<G,F,E,D,S>]
Goal reached!

*UCS:
       Expanded      Queue
          S          [0<S>]
          A          [3.0<A,S> 4.0<D,S>]
          D          [4.0<D,S> 7.0<B,A,S> 8.0<D,A,S>]
          E          [6.0<E,D,S> 7.0<B,A,S> 8.0<D,A,S> 9.0<A,D,S>]
          B          [7.0<B,A,S> 8.0<D,A,S> 9.0<A,D,S> 10.0<F,E,D,S> 11.0<B,E,D,S>]
          D          [8.0<D,A,S> 9.0<A,D,S> 10.0<F,E,D,S> 11.0<B,E,D,S> 11.0<C,B,A,S> 12.0<E,B,A,S>]
          A          [9.0<A,D,S> 10.0<E,D,A,S> 10.0<F,E,D,S> 11.0<B,E,D,S> 11.0<C,B,A,S> 12.0<E,B,A,S>]
          E          [10.0<E,D,A,S> 10.0<F,E,D,S> 11.0<B,E,D,S> 11.0<C,B,A,S> 12.0<E,B,A,S> 13.0<B,A,D,S>]
          F          [10.0<F,E,D,S> 11.0<B,E,D,S> 11.0<C,B,A,S> 12.0<E,B,A,S> 13.0<B,A,D,S> 14.0<F,E,D,A,S> 15.0<B,E,D,A,S>]
          B          [11.0<B,E,D,S> 11.0<C,B,A,S> 12.0<E,B,A,S> 13.0<B,A,D,S> 13.0<G,F,E,D,S> 14.0<F,E,D,A,S> 15.0<B,E,D,A,S>]
          C          [11.0<C,B,A,S> 12.0<E,B,A,S> 13.0<B,A,D,S> 13.0<G,F,E,D,S> 14.0<F,E,D,A,S> 15.0<A,B,E,D,S> 15.0<B,E,D,A,S> 15.0<C,B,E,D,S>]
          E          [12.0<E,B,A,S> 13.0<B,A,D,S> 13.0<G,F,E,D,S> 14.0<F,E,D,A,S> 15.0<A,B,E,D,S> 15.0<B,E,D,A,S> 15.0<C,B,E,D,S>]
          B          [13.0<B,A,D,S> 13.0<G,F,E,D,S> 14.0<D,E,B,A,S> 14.0<F,E,D,A,S> 15.0<A,B,E,D,S> 15.0<B,E,D,A,S> 15.0<C,B,E,D,S> 16.0<F,E,B,A,S>]
          G          [13.0<G,F,E,D,S> 14.0<D,E,B,A,S> 14.0<F,E,D,A,S> 15.0<A,B,E,D,S> 15.0<B,E,D,A,S> 15.0<C,B,E,D,S> 16.0<F,E,B,A,S> 17.0<C,B,A,D,S> 18.0<E,B,A,D,S>]
Goal reached!

*GS:
       Expanded      Queue
          S          [11.0<S>]
          D          [8.9<D,S> 10.4<A,S>]
          E          [6.9<E,D,S> 10.4<A,S> 10.4<A,D,S>]
          F          [3.0<F,E,D,S> 6.7<B,E,D,S> 10.4<A,S> 10.4<A,D,S>]
          G          [0.0<G,F,E,D,S> 6.7<B,E,D,S> 10.4<A,S> 10.4<A,D,S>]
Goal reached!

*ASS:
       Expanded      Queue
          S          [11.0<S>]
          D          [12.9<D,S> 13.4<A,S>]
          E          [12.9<E,D,S> 13.4<A,S>]
          F          [13.0<F,E,D,S> 13.4<A,S> 17.7<B,E,D,S>]
          G          [13.0<G,F,E,D,S> 13.4<A,S> 17.7<B,E,D,S>]
Goal reached!

*HC:
       Expanded      Queue
          S          [11.0<S>]
          D          [8.9<D,S> 10.4<A,S>]
          E          [6.9<E,D,S> 10.4<A,D,S>]
          F          [3.0<F,E,D,S> 6.7<B,E,D,S>]
          G          [0.0<G,F,E,D,S>]
Goal reached!

*BS:
       Expanded      Queue
          S          [11.0<S>]
          A          [10.4<A,S> 8.9<D,S>]
          D          [8.9<D,S> 6.7<B,A,S> 8.9<D,A,S>]
          B          [6.7<B,A,S> 6.9<E,D,S>]
          E          [6.9<E,D,S> 4.0<C,B,A,S> 6.9<E,B,A,S>]
          C          [4.0<C,B,A,S> 3.0<F,E,D,S>]
          F          [3.0<F,E,D,S>]
          G          [0.0<G,F,E,D,S>]
Goal reached!

************************************************************************************************************
**********************************OUTPUT FROM "second_graph.txt"********************************************
************************************************************************************************************

*DFS:
       Expanded      Queue
          S          [<S>]
          A          [<A,S> <T,S> <Z,S>]
          F          [<F,A,S> <O,A,S> <R,A,S> <T,S> <Z,S>]
          G          [<G,F,A,S> <O,A,S> <R,A,S> <T,S> <Z,S>]
Goal reached!

*BFS:
       Expanded      Queue
          S          [<S>]
          A          [<A,S> <T,S> <Z,S>]
          T          [<T,S> <Z,S> <F,A,S> <O,A,S> <R,A,S>]
          Z          [<Z,S> <F,A,S> <O,A,S> <R,A,S> <L,T,S>]
          F          [<F,A,S> <O,A,S> <R,A,S> <L,T,S> <O,Z,S>]
          O          [<O,A,S> <R,A,S> <L,T,S> <O,Z,S> <G,F,A,S>]
          R          [<R,A,S> <L,T,S> <O,Z,S> <G,F,A,S> <Z,O,A,S>]
          L          [<L,T,S> <O,Z,S> <G,F,A,S> <Z,O,A,S> <C,R,A,S> <P,R,A,S>]
          O          [<O,Z,S> <G,F,A,S> <Z,O,A,S> <C,R,A,S> <P,R,A,S> <M,L,T,S>]
          G          [<G,F,A,S> <Z,O,A,S> <C,R,A,S> <P,R,A,S> <M,L,T,S> <A,O,Z,S>]
Goal reached!

*DLS:
       Expanded      Queue
          S          [<S>]
          A          [<A,S> <T,S> <Z,S>]
          F          [<F,A,S> <O,A,S> <R,A,S> <T,S> <Z,S>]
          O          [<O,A,S> <R,A,S> <T,S> <Z,S>]
          R          [<R,A,S> <T,S> <Z,S>]
          T          [<T,S> <Z,S>]
          L          [<L,T,S> <Z,S>]
          Z          [<Z,S>]
          O          [<O,Z,S>]
Path not found :(

*IDS:
       Expanded      Queue

L=0       S          [<S>]

L=1       S          [<S>]
          A          [<A,S> <T,S> <Z,S>]
          T          [<T,S> <Z,S>]
          Z          [<Z,S>]

L=2       S          [<S>]
          A          [<A,S> <T,S> <Z,S>]
          F          [<F,A,S> <O,A,S> <R,A,S> <T,S> <Z,S>]
          O          [<O,A,S> <R,A,S> <T,S> <Z,S>]
          R          [<R,A,S> <T,S> <Z,S>]
          T          [<T,S> <Z,S>]
          L          [<L,T,S> <Z,S>]
          Z          [<Z,S>]
          O          [<O,Z,S>]

L=3       S          [<S>]
          A          [<A,S> <T,S> <Z,S>]
          F          [<F,A,S> <O,A,S> <R,A,S> <T,S> <Z,S>]
          G          [<G,F,A,S> <O,A,S> <R,A,S> <T,S> <Z,S>]
Goal reached!

*UCS:
       Expanded      Queue
          S          [0<S>]
          Z          [75.0<Z,S> 118.0<T,S> 140.0<A,S>]
          T          [118.0<T,S> 140.0<A,S> 146.0<O,Z,S>]
          A          [140.0<A,S> 146.0<O,Z,S> 229.0<L,T,S>]
          O          [146.0<O,Z,S> 220.0<R,A,S> 229.0<L,T,S> 239.0<F,A,S> 291.0<O,A,S>]
          R          [220.0<R,A,S> 229.0<L,T,S> 239.0<F,A,S> 291.0<O,A,S> 297.0<A,O,Z,S>]
          L          [229.0<L,T,S> 239.0<F,A,S> 291.0<O,A,S> 297.0<A,O,Z,S> 317.0<P,R,A,S> 366.0<C,R,A,S>]
          F          [239.0<F,A,S> 291.0<O,A,S> 297.0<A,O,Z,S> 299.0<M,L,T,S> 317.0<P,R,A,S> 366.0<C,R,A,S>]
          O          [291.0<O,A,S> 297.0<A,O,Z,S> 299.0<M,L,T,S> 317.0<P,R,A,S> 366.0<C,R,A,S> 450.0<G,F,A,S>]
          A          [297.0<A,O,Z,S> 299.0<M,L,T,S> 317.0<P,R,A,S> 362.0<Z,O,A,S> 366.0<C,R,A,S> 450.0<G,F,A,S>]
          M          [299.0<M,L,T,S> 317.0<P,R,A,S> 362.0<Z,O,A,S> 366.0<C,R,A,S> 377.0<R,A,O,Z,S> 396.0<F,A,O,Z,S> 450.0<G,F,A,S>]
          P          [317.0<P,R,A,S> 362.0<Z,O,A,S> 366.0<C,R,A,S> 374.0<D,M,L,T,S> 377.0<R,A,O,Z,S> 396.0<F,A,O,Z,S> 450.0<G,F,A,S>]
          Z          [362.0<Z,O,A,S> 366.0<C,R,A,S> 374.0<D,M,L,T,S> 377.0<R,A,O,Z,S> 396.0<F,A,O,Z,S> 418.0<G,P,R,A,S> 450.0<G,F,A,S> 455.0<C,P,R,A,S>]
          C          [366.0<C,R,A,S> 374.0<D,M,L,T,S> 377.0<R,A,O,Z,S> 396.0<F,A,O,Z,S> 418.0<G,P,R,A,S> 450.0<G,F,A,S> 455.0<C,P,R,A,S>]
          D          [374.0<D,M,L,T,S> 377.0<R,A,O,Z,S> 396.0<F,A,O,Z,S> 418.0<G,P,R,A,S> 450.0<G,F,A,S> 455.0<C,P,R,A,S> 486.0<D,C,R,A,S> 504.0<P,C,R,A,S>]
          R          [377.0<R,A,O,Z,S> 396.0<F,A,O,Z,S> 418.0<G,P,R,A,S> 450.0<G,F,A,S> 455.0<C,P,R,A,S> 486.0<D,C,R,A,S> 494.0<C,D,M,L,T,S> 504.0<P,C,R,A,S>]
          F          [396.0<F,A,O,Z,S> 418.0<G,P,R,A,S> 450.0<G,F,A,S> 455.0<C,P,R,A,S> 474.0<P,R,A,O,Z,S> 486.0<D,C,R,A,S> 494.0<C,D,M,L,T,S> 504.0<P,C,R,A,S> 523.0<C,R,A,O,Z,S>]
          G          [418.0<G,P,R,A,S> 450.0<G,F,A,S> 455.0<C,P,R,A,S> 474.0<P,R,A,O,Z,S> 486.0<D,C,R,A,S> 494.0<C,D,M,L,T,S> 504.0<P,C,R,A,S> 523.0<C,R,A,O,Z,S> 607.0<G,F,A,O,Z,S>]
Goal reached!

*GS:
       Expanded      Queue
          S          [366.0<S>]
          A          [253.0<A,S> 329.0<T,S> 374.0<Z,S>]
          F          [178.0<F,A,S> 193.0<R,A,S> 329.0<T,S> 374.0<Z,S> 380.0<O,A,S>]
          G          [0.0<G,F,A,S> 193.0<R,A,S> 329.0<T,S> 374.0<Z,S> 380.0<O,A,S>]
Goal reached!

*ASS:
       Expanded      Queue
          S          [366.0<S>]
          A          [393.0<A,S> 447.0<T,S> 449.0<Z,S>]
          R          [413.0<R,A,S> 417.0<F,A,S> 447.0<T,S> 449.0<Z,S> 671.0<O,A,S>]
          P          [415.0<P,R,A,S> 417.0<F,A,S> 447.0<T,S> 449.0<Z,S> 526.0<C,R,A,S> 671.0<O,A,S>]
          F          [417.0<F,A,S> 418.0<G,P,R,A,S> 447.0<T,S> 449.0<Z,S> 526.0<C,R,A,S> 671.0<O,A,S>]
          G          [418.0<G,P,R,A,S> 447.0<T,S> 449.0<Z,S> 526.0<C,R,A,S> 671.0<O,A,S>]
Goal reached!

*HC:
       Expanded      Queue
          S          [366.0<S>]
          A          [253.0<A,S> 329.0<T,S> 374.0<Z,S>]
          F          [178.0<F,A,S> 193.0<R,A,S> 380.0<O,A,S>]
          G          [0.0<G,F,A,S>]
Goal reached!

*BS:
       Expanded      Queue
          S          [366.0<S>]
          A          [253.0<A,S> 329.0<T,S>]
          T          [329.0<T,S> 178.0<F,A,S> 380.0<O,A,S> 193.0<R,A,S>]
          F          [178.0<F,A,S> 193.0<R,A,S>]
          R          [193.0<R,A,S> 0.0<G,F,A,S>]
          G          [0.0<G,F,A,S> 98.0<P,R,A,S>]
Goal reached!