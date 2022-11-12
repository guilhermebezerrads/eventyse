import { Post } from "src/models/post.model"

export class PostMock {
  static mockPost1: Post = {
    author: {
      name: "Sasuke", profileImage: "assets/palmirinha.png"
    },
    title: "Melhores pães de queijo de Boston",
    description: "Oi pessoal, visitei Boston recentemente e marquei aqui os melhores pães de queijo da cidade! Eu amo demais demais demais pão de queijo!",
    creationDate: new Date(2022, 1, 1, 13, 13),
    tags: ["boston", "estadosunidos", "paodequeijo"],
    countDislike: 43,
    countLike: 123,
    comments: [
      {
        author: {
          name: "Sasuke", profileImage: "assets/palmirinha.png"
        },
        comment: "Odeio pão de queijo!",
        createDate: new Date(2022, 1, 1, 23, 13)
      },
      {
        author: {
          name: "Sasuke", profileImage: "assets/palmirinha.png"
        },
        comment: "Amo pão de queijo!",
        createDate: new Date(2022, 1, 1, 23, 35)
      },
    ],
    map: {
       coordinates: [
        [39.8282,  -98.5795],
        [36.2017372066406,  -94.00780498981477],
        [39.259485302277554,  -85.39452373981477],
        [42.966075955988025,  -101.56639873981477],
        [40.339850993496356,  -113.51952373981477],
       ]
    }
  }

  static mockPost2: Post = {
    author: {
      name: "Sasuke", profileImage: "assets/palmirinha.png"
    },
    title: "Melhores pães de queijo de Boston",
    description: "Oi pessoal, visitei Boston recentemente e marquei aqui os melhores pães de queijo da cidade!",
    creationDate: new Date(2022, 1, 1, 13, 13),
    tags: ["boston", "estadosunidos", "paodequeijo"],
    countDislike: 43,
    countLike: 123,
    comments: [
      {
        author: {
          name: "Sasuke", profileImage: "assets/palmirinha.png"
        },
        comment: "Odeio pão de queijo!",
        createDate: new Date(2022, 1, 1, 23, 13)
      },
      {
        author: {
          name: "Sasuke", profileImage: "assets/palmirinha.png"
        },
        comment: "Amo pão de queijo!",
        createDate: new Date(2022, 1, 1, 23, 35)
      },
    ],
    map: {
       coordinates: [
        [39.8282,  -98.5795],
        [36.2017372066406,  -94.00780498981477],
        [39.259485302277554,  -85.39452373981477],
        [42.966075955988025,  -101.56639873981477],
        [40.339850993496356,  -113.51952373981477],
       ]
    }
  }
}
